---
sidebar_position: 3
---

#  Student Portal Frontend (Next.js)

The Student Portal is a modern, responsive frontend application built with Next.js. It provides parents with a secure and easy-to-use interface to view and pay school fees.

To build the student portal, we will use a separate frontend application built with Next.js. A starter repository is provided to give you the basic structure, UI components, and API service helpers.

:::info
**Action Required: Clone the Starter Repository**

[➡️ TODO: Insert Git repository link here](https://git.logicloop.io/asifLogicloop/school-fees-portal-frontend)

Clone this repository to your local machine.
:::

## Login and Authentication

The portal uses a secure, OTP-based login system.

-   **Login Method**: Parents use their registered email address to log in.
-   **OTP Verification**: Upon entering their email, they receive a One-Time Password (OTP) to that email address. Entering the correct OTP grants them access to the portal.

This method is secure and convenient, as parents don't need to remember a password.

```Typescript
// src/store/services/studentApi.ts
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const studentApi = createApi({
  reducerPath: "studentApi",
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.NEXT_PUBLIC_BACKEND_API_URL,
    prepareHeaders: (headers) => {
      const token = localStorage.getItem("token"); // or sessionStorage
      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
      return headers;
    },
}),
  endpoints: (builder) => ({
    // Step 1: Validate student
    validateStudent: builder.query({
      query: (studentLoginId: string) => `api/student/login/initiate/${studentLoginId}`,
    }),
  })
})
```
![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/student.png)

## Dashboard

After logging in, the parent is directed to the main dashboard. The dashboard is designed to provide a clear overview of their fee status and payment history.

A header is always visible at the top, containing a link to the user's profile section.

The dashboard is organized into four tabs:

### Due Payments
This is the default tab. It displays a list of all outstanding fee payments. Each item shows:
- Fee Type (e.g., Tuition Fee, Sports Fee)
- Amount Due
- Due Date
- A "Pay Now" button


![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/sp-due.png)

### Transaction History
This tab shows a complete history of all payment attempts made by the parent, including successful, failed, and pending transactions. This provides a comprehensive audit trail.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/sp-cash.png)

###  Transactions Details
This tab provides a view of all transactions associated with the student, which can be useful for reconciliation purposes.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/transaction-details.png)

### Cancelled Payments
This tab lists any payments that were initiated but subsequently cancelled either by the user or the system.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/sp-cancel.png)

## Profile Management

The profile page allows parents to manage their contact information.

-   **URL**: `/profile`
-   **Editable Fields**:
    -   Parent's Name
    -   Parent's Email Address (for login and notifications)
    -   Parent's Mobile Number


![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/sp-profile-new.png)

## Other Pages

The portal also includes standard static pages, which can be customized.

-   `/privacyPolicy`: To display the institute's privacy policy.
-   `/faq`: For frequently asked questions about the fee payment process.
-   `/termsandcondition`: To display the institute's terms and conditions.

These pages are essential for providing comprehensive information and support to the users.
