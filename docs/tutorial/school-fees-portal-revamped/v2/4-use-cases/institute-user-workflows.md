---
sidebar_position: 2
---

# 2. Institute User Workflows

This section covers the primary workflows for an institute's administrative user, from logging in to managing payments.

## User Login and Access Control

An `InstituteUser` is a user who belongs to a specific institute. Their access must be strictly limited to their own institute's data.

### The Magic of Security Record Rules

SolidX achieves this data isolation not by writing complex queries in every service, but by using **Security Record Rules**. These are powerful, metadata-driven rules that automatically filter data for a user based on their role and relationships.

**Example Rule:**

-   **Goal:** An Institute Admin should only see students from their own institute.
-   **Rule Logic:** "For a user with the 'Institute Admin' role, when they query for `Student` records, only return the records where the `Student`'s `institute` field matches the `institute` field of the logged-in user's own `InstituteUser` record."

This is configured once in the **Solid Core > Security > Security Record Rule** section of the admin panel. After that, every query, API call, and list view is automatically and securely filtered, providing robust multi-tenancy out of the box.

:::tip
A screenshot of the "Add/Edit Security Record Rule" UI from the admin panel would be very effective here.
:::

## User Dashboard

Upon logging in, the Institute Admin should be greeted with a dashboard providing an at-a-glance view of the institute's financial health.

:::tip
A mockup or screenshot of this dashboard UI would be very effective here.
:::

### Key Metrics on the Dashboard

-   **Total Collected:** A sum of all successful payments for the current academic year.
-   **Total Outstanding:** The total amount pending from all students.
-   **Total Overdue:** The portion of the outstanding amount that is past its due date.
-   **Recent Transactions:** A list of the 5-10 most recent payment activities (successful or failed).
-   **Quick Actions:** Buttons to "Start a New Payment Collection" or "View All Students".

## Bulk Data Upload via Excel

This is the primary method for an institute to initiate a large number of fee requests at once.

### Business Reason

Manually creating hundreds of fee records is inefficient and error-prone. A bulk upload feature allows admins to work in a familiar tool like Excel and import everything in a single action.

### Process Flow

```mermaid
graph TD
    A[Admin navigates to <br> 'Payment Collections' and clicks 'Add'] --> B{Fills in Collection Name <br> e.g., "Spring 2024 Fees"};
    B --> C{Uploads Excel/CSV file <br> to the 'Payment File' field};
    C --> D[Admin saves the Payment Collection];
    D -- Triggers Event --> E((SolidX Backend));
    E -- 'afterInsert' event --> F{MediaTransactionSubscriber <br> starts processing};
    F --> G{Reads and validates <br> each row of the Excel file};
    G --> H{For each row: <br> 1. Find or Create Student <br> 2. Create PaymentCollectionItem};
    H --> I[Processing Complete];
    I --> J[Emails are sent to all <br> parents/students about the new fees];
```

### Excel File Format

The system's subscriber will expect the uploaded Excel file to have a specific set of columns.

| Column Header | Example | Description |
|---|---|---|
| `student_id` | `STU-1023` | The unique ID of the student in the institute. |
| `student_name` | `Jane Doe` | Full name of the student. Used if the student doesn't exist yet. |
| `parent_email` | `parent@example.com` | Parent's email. Used for notifications and creating new students. |
| `fee_type` | `Tuition Fee` | The name of the fee. Must match a `FeeType` already configured for the institute. |
| `amount` | `1500.00` | The amount due for this specific fee. |
| `due_date` | `2024-09-01` | The date the payment is due (YYYY-MM-DD). |

## Initiating a Single Payment

While bulk uploads are common, admins may also need to create a one-off fee request for a single student (e.g., for a library fine or a special event).

This is done directly through the UI by navigating to the **Payment Collection Items** model, clicking "Add", and filling in the details manually, linking the student and fee type. Saving the record would trigger the same email notification as the bulk upload.

## Canceling a Payment

Admins may need to cancel a fee request that was created in error.

1.  The admin navigates to the specific `PaymentCollectionItem` record.
2.  They select a "Cancel" action from the record's context menu or a button on the page.
3.  The system updates the `status` of the `PaymentCollectionItem` to `Cancelled`.
4.  This item will no longer appear in the student's list of outstanding fees.
5.  **Note:** This action is only possible for fees that have not yet been paid. If a payment has been made, a formal "Refund" process must be initiated instead.
