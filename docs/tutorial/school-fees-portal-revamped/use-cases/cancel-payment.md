---
sidebar_position: 4
---

# Cancel Payment Workflow

In any financial system, flexibility is key. The Cancel Payment workflow provides Institute Administrators with the essential ability to reverse pending payment requests. This might be necessary due to data entry errors, duplicate requests, or changes in a student's enrollment status. This guide details the user-facing methods for cancellation and provides an in-depth explanation of the underlying backend logic.

## User Journey: How to Cancel Payments

An Institute Admin can cancel payments using two distinct methods, providing flexibility for both targeted and bulk actions.

#### 1. Individual or Multiple Selection

For precise control, the admin can select one or more payment items directly from the list using checkboxes and then click the "Cancel Payment" button.

![Cancel by Checkbox](/img/tutorial/school-fees-portal/6-usecase/cancel1.png)

#### 2. Bulk Cancellation by Filter

For broader actions, the admin can first apply filters (e.g., by student, date range, or fee type) to narrow down the list of payments.

![Apply Filters for Cancellation](/img/tutorial/school-fees-portal/6-usecase/cancel3.png)

After applying filters, clicking the "Cancel" button will trigger a confirmation pop-up. Confirming this action will cancel all the items matching the filter criteria.

![Confirm Bulk Cancellation](/img/tutorial/school-fees-portal/6-usecase/cancel2.png)

## Backend Implementation Deep Dive

The core logic for this feature is handled by the `cancelPaymentCollectionItems` method in the backend service. Let's break down how it works.

### Method Signature

The method is designed to handle cancellations originating from different contexts, accepting IDs of parent `PaymentCollection` records, child `PaymentCollectionItem` records, or a set of filters.

```typescript
async cancelPaymentCollectionItems(
    collectionIds: string[] = [],  // IDs of parent PaymentCollection records
    itemIds: string[] = [],        // IDs of child PaymentCollectionItem records
    filters: Record<string, any> = {}, // Filters from the UI
    modelName: string              // The context, e.g., "paymentCollection"
) {
```

### 1. Building the Query

The first step is to construct a robust database query that correctly identifies the payment items to be cancelled. The logic handles multiple scenarios:

-   It validates that at least one source of filters (`collectionIds`, `itemIds`, or `filters`) is provided.
-   It ensures that only items with a `Pending` status are targeted.
-   It combines the provided IDs and UI filters into a single, cohesive query.

```typescript
    let combinedFilters: any;

    // Logic for cancellations initiated from the main PaymentCollection view
    if (modelName === "paymentCollection") {
      if (!collectionIds.length && (await this.isFiltersEmpty(filters))) {
        throw new BadRequestException("Either collectionIds or filters must be provided");
      }
      const baseAnd = [
        { status: { $eq: "Pending" } },
        ...(collectionIds.length ? [{ paymentCollection: { id: { $in: collectionIds } } }] : []),
      ];
      const transformedFilters = collectionIds.length ? filters : await this.transformFilters(filters, "paymentCollection");
      const filtersAndArray: any[] = [...baseAnd];
      if (Object.keys(transformedFilters).length > 0) {
        filtersAndArray.push(transformedFilters);
      }
      combinedFilters = { $and: filtersAndArray };

    // Logic for cancellations initiated from the PaymentCollectionItem view
    } else if (modelName === "paymentCollectionItem") {
      if (!itemIds.length && (await this.isFiltersEmpty(filters))) {
        throw new BadRequestException("Either itemIds or filters must be provided");
      }
      const baseAnd = [
        { status: { $eq: "Pending" } },
        ...(itemIds.length ? [{ id: { $in: itemIds } }] : []),
      ];
      const filtersAndArray: any[] = [...baseAnd];
      if (Object.keys(filters).length > 0) {
        filtersAndArray.push(filters);
      }
      combinedFilters = { $and: filtersAndArray };
    }
    // ...
```

### 2. Fetching and Validating Records

With the query constructed, the service fetches all matching `PaymentCollectionItem` records. It uses `populate` to also retrieve related data like student, institute, and fee type details, which are needed for sending email notifications. If no eligible records are found, it throws an error.

```typescript
    const cleanedFilters = cleanNullsFromObject(combinedFilters);
    const query = {
      filters: cleanedFilters,
      populate: ["institute", "student", "feeType", "paymentCollection"],
      populateMedia: ["institute.logo"],
    };

    const pendingItemsData = await this.find(query);
    const pendingItems = pendingItemsData.records;

    if (!pendingItems?.length) {
      throw new BadRequestException("No eligible records found for cancellation");
    }
```

### 3. Bulk Update

This is the critical step where the database is updated. The service performs a bulk update operation, changing the `status` of all identified payment items to `"Cancelled"` in a single, efficient query.

```typescript
    const pendingIds = pendingItems.map((item) => item.id);

    try {
      // Bulk cancel the items in the database
      await this.repo.update({ id: In(pendingIds) }, { status: "Cancelled" });
```

### 4. Sending Email Notifications

After successfully cancelling the items, the system notifies the parents.

-   The code groups the cancelled items by the parent's email address to send a single, consolidated email per parent.
-   It then iterates through this map, calculates the total cancelled amount for each parent, and constructs the payload for the email.
-   Finally, it uses a mail service to send an email based on the `cancel-payment` template, including all relevant details.

```typescript
      // Group items by parent email to send one notification per parent
      const itemsByParent = new Map<string, any>();
      pendingItems.forEach((item) => {
        const parentEmail = item.student?.parentEmailAddress;
        if (!parentEmail) return;

        if (!itemsByParent.has(parentEmail)) {
          itemsByParent.set(parentEmail, { student: item.student, institute: item.institute, items: [] });
        }
        itemsByParent.get(parentEmail).items.push(item);
      });

      // Send email notifications asynchronously
      const mailService = this.mailServiceFactory.getMailService();
      for (const [parentEmail, data] of itemsByParent) {
          // ... logic to calculate totalAmount, feeTypes etc. ...

          await mailService.sendEmailUsingTemplate(
              parentEmail,
              "cancel-payment",
              { /* ... email payload with student and payment details ... */ },
              true
            );
      }
```

### 5. Returning the Result

The method returns a detailed success message, including a list of the cancelled items and their IDs, which the frontend can use to update the UI.

```typescript
      return {
        success: true,
        message: `Successfully cancelled ${pendingIds.length} payment collection item(s)`,
        cancelledIds: pendingIds,
        emailsSent: itemsByParent.size,
      };
    } catch (error) {
      // ... error handling ...
    }
```

## Key Business Rules

The cancellation process adheres to the following critical rules:

-   **Status Constraint:** Only payment items with a `Pending` status are eligible for cancellation.
-   **Parental Notification:** The system automatically groups all cancelled items for a student and sends a single, consolidated email notification to the parent.
-   **Data Integrity:** Cancelled payments are flagged and excluded from all future financial calculations and reports.
-   **Auditing:** Every cancellation action is logged, providing a clear audit trail for financial accountability.
