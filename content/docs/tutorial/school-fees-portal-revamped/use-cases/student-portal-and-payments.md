---
title: Student Portal Frontend (Next.js)
---

The Student Portal is a modern, responsive frontend application built with Next.js. It provides parents with a secure and easy-to-use interface to view and pay school fees.

To build the student portal, we will use a separate frontend application built with Next.js. A starter repository is provided to give you the basic structure, UI components, and API service helpers.

> **Info**
> **Action Required: Clone the [Starter Repository](https://github.com/SolidXAI/student-portal-next-js.git)**
> 
> Clone this repository to your local machine.

## Setup

After cloning the repository, navigate to the project directory and install the necessary dependencies using `npm`:

```bash
cd student-portal-next-js
npm install
```

Once the installation is complete, create .env in root and Add

```bash
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:3000
```
you can run the development server:

```bash
npm run dev
```

Your application will run on the following default ports:

```text
Solid API Server  : http://localhost:3000  
Solid UI          : http://localhost:3001  
Student Portal    : http://localhost:3002
```

The Student Portal is now accessible at:

```text
http://localhost:3002
```

## Local Development with Nginx Proxy

For a seamless local development experience that mirrors a production multi-tenant environment, you can use Nginx as a reverse proxy. This setup forwards requests made to a local domain to your Next.js application.

Here are the steps to configure Nginx:

#### Step 1: Create Nginx Configuration

First, create a new Nginx configuration file for your student portal site. You can use a text editor like `vi` or `nano`:

```bash 
sudo nano /etc/nginx/sites-available/test-edu.domain
```

Add the following server block to the file. This configures Nginx to listen on port 80 for requests to `test-edu.domain` and proxy them to your Next.js app running on port 3002.

```nginx
server {
    listen 80;
    server_name test-edu.domain;

    location / {
        proxy_pass http://127.0.0.1:3002;
        proxy_http_version 1.1;

        # Forward real IP & headers
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_redirect off;
    }
}
```

#### Step 2: Update Hosts File

Next, map the custom domain to your local machine by adding an entry to your `/etc/hosts` file.

```bash
sudo nano /etc/hosts
```

Add the following line to the file:
```
127.0.0.1    test-edu.domain
```

This tells your system to resolve `test-edu.domain` to your local machine.

#### Step 3: Enable the Site

Create a symbolic link from your configuration file in `sites-available` to the `sites-enabled` directory. This tells Nginx to serve this site.

```bash
sudo ln -s /etc/nginx/sites-available/test-edu.domain /etc/nginx/sites-enabled
```

#### Step 4: Restart Nginx

Finally, apply the changes by restarting the Nginx service.

```bash
sudo systemctl restart nginx
```

Now, when you navigate to `http://test-edu.domain` in your browser, you should see your Student Portal application. 

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/stu-1.png)

> **Info**
> Above **test** is nothing but our hostedPagePrefix which was earlier used to create an Institute.

## Login and Authentication

The portal uses a secure, two-step login process involving a unique student ID and a One-Time Password (OTP).

-   **Login Method**: Students or parents log in using a unique **Student Login ID**. This ID is automatically pre-filled when they click the "Pay Now" button in a fee notification email.
-   **OTP Verification**: After entering the Student Login ID, an OTP is sent to the parent's registered email address. Entering the correct OTP grants access to the portal.

This passwordless method is both secure and convenient.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/stu-2.png)

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/stu-3.png)

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/stu-4.png)

To implement this, you can create a login page at `src/app/page.tsx` with two states: one for entering the student login id and another for verifying the OTP.

Here is an example of how you can structure the component:
<details>
<summary>Complete Source Code for Student Login Screen</summary>

```jsx
"use client";

import { useEffect, useState } from "react";
import { useInitiateOtpMutation } from "@/store/services/studentApi";
import { useLazyValidateStudentQuery } from "@/store/services/studentApi"; // lazy because it’s on button click
import { useRouter } from "next/navigation";
import { showToast } from "@/store/slices/toastSlice";
import { useDispatch } from "react-redux";
import { getHostedPagePrefix } from "@/utils/institute.utils";
import { setInstitute } from "@/store/slices/instituteSlice";
import { useSearchParams } from "next/navigation";

export default function HomePage() {
  const router = useRouter();
  const dispatch = useDispatch();
  const searchParams = useSearchParams();
  const id = searchParams.get("id");
  const [triggerValidate] = useLazyValidateStudentQuery();
  const [initiateOtp] = useInitiateOtpMutation();
  const [studentLoginId, setstudentLoginId] = useState(id || "");
  const [student, setStudent] = useState<{
    email: string;
    mobile: string;
  } | null>(null);
  const [showOtpButton, setShowOtpButton] = useState(false);
  const [isLoading] = useState(false);
  const [hostedPagePrefix, setHostedPagePrefix] = useState("");
  
    useEffect(() => {
      if (typeof window !== "undefined") {
        const hostname = window.location.hostname;
        const prefix = getHostedPagePrefix(hostname);
        setHostedPagePrefix(prefix);
      }
    }, []);

    
  useEffect(() => {
    if (!id) return;

    // Read current path
    const path = window.location.pathname;

    // Clone search params & remove id
    const params = new URLSearchParams(searchParams.toString());
    params.delete("id");

    const newUrl = params.toString() ? `${path}?${params.toString()}` : path;

    router.replace(newUrl, { scroll: false });
  }, [id]);

  const handleFetch = async () => {
    if (!studentLoginId.trim()) {
      dispatch(
        showToast({
          severity: "warn",
          summary: "",
          detail: "Please Enter a Student ID.",
        })
      );
      return;
    }

    // alert('Please enter a Student ID');
    const result = await triggerValidate(studentLoginId)
      .unwrap()
      .catch(() => {
        dispatch(
          showToast({
            severity: "error",
            summary: "",
            detail: "Invalid Student ID.",
          })
        );
      });
    if (result?.data?.isValid) {
      setStudent({
        email: result?.data?.maskedEmail,
        mobile: result?.data?.maskedPhone,
      });
      setShowOtpButton(true);
    } else {
      dispatch(
        showToast({
          severity: "error",
          summary: "",
          detail: "Invalid Student ID.",
        })
      );
    }
  };

  const handleOtp = async () => {
    try {
      const result = await initiateOtp(studentLoginId).unwrap();
      if (result?.data?.success) {
        localStorage.setItem("studentLoginId", studentLoginId);
        localStorage.setItem("id", result?.data?.id);
        dispatch(
          showToast({
            severity: "success",
            summary: "",
            detail: "Otp is sent on your email.",
          })
        );
        router.push("/otp");
      }
    } catch (err) {
      console.log("Failed to send OTP", err);
    }
  };

    useEffect(() => {
      if (hostedPagePrefix) {
        fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_API_URL}/api/institute/public/${hostedPagePrefix}`
        )
          .then((res) => res.json())
          .then((response) => {
            if (response.data) {
              dispatch(setInstitute(response.data));
            }
          });
      }
    }, [hostedPagePrefix, dispatch]);

  return (
    <div>
      {/* Centered Main Content */}
      <div>
        <div>
          {/* Login Card */}
          <div>
            <div>
              Sign In To Your Account
              <p>
                Sign in to view the payment details
              </p>
            </div>

            <div>
              {/* Student ID Input */}
              {!showOtpButton && (
                <div>
                  <label
                    htmlFor="studentLoginId"
                   
                  >
                    Student Login ID
                  </label>
                  <input
                    type="text"
                   
                    id="studentLoginId"
                    placeholder="Type here"
                    value={studentLoginId}
                    onChange={(e) => setstudentLoginId(e.target.value)}
                  />
                </div>
              )}

              {/* Student Details Display */}
              {student && (
                <div>
                  <div>
                    <p>
                      Please confirm your registered email 
                      We’ll send an OTP to these for verification and login.
                    </p>
                  </div>
                  <div>
                    <span>
                      Parent Email:
                    </span>
                    <span>
                      {student.email}
                    </span>
                  </div>
                </div>
              )}
              {/* Action Buttons */}
              {!showOtpButton ? (
                <button
                 
                  onClick={handleFetch}
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <span
                       
                        role="status"
                      ></span>
                      Loading...
                    </>
                  ) : (
                    "Login"
                  )}
                </button>
              ) : (
                <div>
                  <button
                   
                    onClick={() => {
                      setShowOtpButton(false);
                      setStudent(null);
                      setstudentLoginId("");
                    }}
                  >
                    <i></i>Back
                  </button>
                  <button
                   
                    onClick={handleOtp}
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>
                        <span
                         
                          role="status"
                        ></span>
                        Processing...
                      </>
                    ) : (
                      <>
                        <i></i>
                        Send OTP
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

```
</details>

This component manages the UI state for the login process. When the user first lands on the page, they see the email form. After submitting their email, the UI switches to the OTP verification form. The `handleEmailSubmit` and `handleOtpSubmit` functions are where you would integrate your API calls.

## Dashboard

After logging in, the parent is directed to the main dashboard. The dashboard is designed to provide a clear overview of their fee status and payment history.

A header is always visible at the top, containing a link to the user's profile section.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/stu-5.png)

The dashboard is organized into four main tabs to provide a comprehensive overview of the student's financial activities:

-   **Due Payments**: Displays all outstanding payments that have been initiated by the institute. This is the default view.
-   **Payment History**: Shows a complete record of all payments made, including both online (payment gateway) and offline transactions.
-   **Transaction Details**: Provides a detailed log of all online payment gateway transactions, including their status (e.g., failed, pending, successful).
-   **Cancelled Payments**: Lists any payments that were initiated but subsequently cancelled by either the user or the system. 

The dashboard can be implemented at `src/pages/dashboard.tsx`. Here's how you can structure the layout with tabs:

### Due Payments

This component does the following:
-   Fetches due payments from an API when the component mounts.
-   Handles loading and error states.
-   Renders a list of payments, each with a "Pay Now" button.
-   Includes a `handlePayNow` function to initiate the payment process.
<details>
<summary>Complete Source Code for Dashboard Screen includes Due Payments</summary>

```jsx
"use client";

import {
  ClosedArrowIcon,
  OpenArrowIcon,
  PaymentStatusIcon,
} from "@/utils/App-icons";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  useLazyGetStudentPaymentRecordQuery,
  usePaymentGatwayMutation,
} from "@/store/services/studentApi"; // adjust if path differs
import { setStudentPayments } from "@/store/slices/studentPaymentSlice";
import { RootState } from "@/store";
import { Confirmation } from "@/components/Confirmation";
import { showToast } from "@/store/slices/toastSlice";

interface PaymentCollectionItem {
  id: number;
  amountPaid: number;
  amountPending: number;
  amountToBePaid: number;
  dueDate: string;
  isOverdue: boolean;
  lateAmountToBePaid: number;
  partPaymentAllowed: boolean;
  status: string;
  feeType: {
    id: number;
    name: string;
  };
}

interface StudentPaymentRecord {
  id: number;
  name: string;
  description: string;
  createdOn: string;
  totalAmountToBePaid: number;
  institute: {
    id: number;
    name: string;
  };
  paymentCollectionItems: PaymentCollectionItem[];
}

export default function DashboardPage() {
  const dispatch = useDispatch();
  const student = useSelector((state: RootState) => state.student.data);
  const studentPayments = useSelector(
    (state: RootState) => state.studentPayments.data
  );
  const [PaymentGateway] = usePaymentGatwayMutation();
  const [fetchPayments] = useLazyGetStudentPaymentRecordQuery();
  // const [expandedRefs, setExpandedRefs] = useState<string[]>(["01"]);
  const [expandedRefs, setExpandedRefs] = useState<number[]>([]);
  const [editedPayments, setEditedPayments] = useState<Record<number, number>>(
    {}
  );
  const [totalAmount, setTotalAmount] = useState(0);
  const [initialTotalAmount, setInitialTotalAmount] = useState(0);
  const [paymentStatus, setPaymentStatus] = useState<"success" | "failed" | null>(null);

  useEffect(() => {
    const status = new URLSearchParams(window.location.search).get("paymentStatus");

    if (status === "success" || status === "failed") {
      setPaymentStatus(status as "success" | "failed");

      // clear query param from URL
      const url = new URL(window.location.href);
      url.searchParams.delete("paymentStatus");
      window.history.replaceState({}, "", url.toString());
    }
  }, []);

  const fetchPaymentsAfterSuccess = () => {
      // Re-fetch payments after successful payment
      if (student?.studentLoginId) {
        fetchPayments({ studentLoginId: student.studentLoginId, isPaid: false }).then(
          (res) => {
            if (res?.data?.data) {
              dispatch(setStudentPayments(res.data.data));
              const defaultExpandedIds = res.data.data.map(
                (d: StudentPaymentRecord) => d.id
              );
              setExpandedRefs(defaultExpandedIds);
            }
          }
        );
      }
  }
  useEffect(() => {
    if (student?.studentLoginId) {
      fetchPayments({ studentLoginId: student.studentLoginId, isPaid: false }).then(
        (res) => {
          if (res?.data?.data) {
            dispatch(setStudentPayments(res.data.data));
            const defaultExpandedIds = res.data.data.map(
              (d: StudentPaymentRecord) => d.id
            );
            setExpandedRefs(defaultExpandedIds);
          }
        }
      );
    }
  }, [student?.studentLoginId]);

  useEffect(() => {
    if (!studentPayments) return;

    let total = 0;
    let initialTotal = 0;

    studentPayments.forEach((collection) => {
      collection.paymentCollectionItems.forEach((item) => {
        initialTotal += item.amountPending;
        const amount =
          editedPayments[item.id] !== undefined
            ? editedPayments[item.id]
            : item.amountPending;

        total += amount;
      });
    });
    setInitialTotalAmount(initialTotal);
    setTotalAmount(total);
  }, [editedPayments, studentPayments]);

  const toggleRef = (refId: number) => {
    setExpandedRefs((prev) =>
      prev.includes(refId)
        ? prev.filter((ref) => ref !== refId)
        : [...prev, refId]
    );
  };

  // const handleMakePayment = () => {
  //   alert("Redirecting to payment gateway...");
  // };

  const formatCurrency = (amount: number) => {
    return `₹${amount.toLocaleString()}`;
  };

  const handleMakePayment = async () => {
    const paymentCollectionItemIds: number[] = [];
    const amountMap: Record<number, number> = {};
    let totalAmount = 0;

    studentPayments?.forEach((collection) => {
      collection.paymentCollectionItems.forEach((item) => {
        const amount =
          editedPayments[item.id] !== undefined
            ? editedPayments[item.id]
            : item.amountPending;

        if (amount > 0) {
          paymentCollectionItemIds.push(item.id);
          amountMap[item.id] = amount;
          totalAmount += amount;
        }
      });
    });
    if (paymentCollectionItemIds.length === 0) {
      // alert("Please enter a valid amount to pay.");
      dispatch(
        showToast({
          severity: "error",
          summary: "",
          detail: "Please enter a valid amount to pay.",
        })
      );
      return;
    }
    const studentLoginId = localStorage.getItem("studentLoginId");
    const response = await PaymentGateway({
      studentLoginId: studentLoginId,
      amountMap: amountMap,
      totalAmount: totalAmount,
    });
    if (response?.data?.data?.url) {
      window.location.href = response?.data?.data?.url; // Redirect to Mswipe
    } else {
      dispatch(
        showToast({
          severity: "error",
          summary: "",
          detail: "Payment failed, Please contact to your institute.",
        })
      );
    }
  };
  const isMakePaymentDisabled = studentPayments?.every(
    (collection) =>
      collection.paymentCollectionItems.length === 0 ||
      collection.paymentCollectionItems.every(
        (item) => item.amountPending === 0
      )
  );

  const hasDuePayments = studentPayments?.some((ref) =>
    ref.paymentCollectionItems?.some((item) => item.amountPending > 0)
  );

  return (
    <>
      {paymentStatus ? (
        <div>
          <Confirmation
            status={paymentStatus}
            handleIsOpen={() => {
              if (paymentStatus === "success") {
                fetchPaymentsAfterSuccess();
              }
              setPaymentStatus(null); // close modal
            }}
          />
        </div>
      ) : null}

      <div>
        {/* Payment Due Header */}
        <div>
          <div>
            Due Payments
          </div>
        </div>

        {/* Payment References */}
        {!hasDuePayments ? (
          <p>
            No Due Payments
          </p>
        ) : (
          studentPayments
            ?.filter((ref) =>
              ref.paymentCollectionItems?.some((item) => item.amountPending > 0)
            )
            ?.map((ref) => (
              <div key={ref.id}>
                {/* Reference Header */}
                <div
                 
                  onClick={() => toggleRef(ref.id)}
                >
                  <div>
                    <div>
                      {/*  */}
                      {expandedRefs.includes(ref.id) ? (
                        
                      ) : (
                        
                      )}
                      <span>
                        {" "}
                        <span>
                          {ref.name}
                        </span>
                      </span>
                    </div>
                    <div>
                      <small>
                        Created On: {"  "}
                        <span>
                          {ref.createdOn}
                        </span>
                      </small>
                    </div>
                  </div>
                </div>

                {/* Reference Content */}

                {expandedRefs.includes(ref.id) && (
                  <div>
                    {/* Desktop Table View */}
                    {ref?.paymentCollectionItems?.length === 0 ||
                    isMakePaymentDisabled ? (
                      <>
                        <p>
                          {" "}
                          No Payment Due
                        </p>
                      </>
                    ) : (
                      <div>
                        {/* Table Header */}
                        <div>
                          <div>
                            Fees
                          </div>
                          <div>
                            Original Due Amount
                          </div>
                          <div>
                            Due Date
                          </div>
                          <div>
                            Late Fee Amount
                          </div>
                          <div>
                            Total Amount Due
                          </div>
                          <div>
                            Paid Amount
                          </div>
                          <div>
                            {" "}
                          </div>
                          <div>
                            Status
                          </div>
                        </div>

                        {/* Payment Rows */}

                        {ref?.paymentCollectionItems?.map((item) => {
                          const isOverdue =
                            new Date(item.dueDate.slice(0, 10)).getTime() <
                            new Date(new Date().setHours(0, 0, 0, 0)).getTime();

                          return (
                            <div
                              key={item.id}
                              className={`table-row ${
                                isOverdue ? "fst-italic" : ""
                              }`}
                            >
                              <div>
                                <span
                                  className={`fw-medium ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {item.feeType.name}
                                </span>
                              </div>
                              <div>
                                <span
                                  className={`fw-medium ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {formatCurrency(item.amountToBePaid)}
                                </span>
                              </div>
                              <div>
                                <span
                                  className={`fw-medium ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {item.dueDate}
                                </span>
                              </div>
                              <div>
                                <span
                                  className={`fw-medium ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {formatCurrency(item.lateAmountToBePaid)}
                                </span>
                              </div>
                              <div>
                                <span
                                  className={`fw-medium ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {formatCurrency(item.amountPending)}
                                </span>
                              </div>
                              <div>
                                <span
                                  className={`fw-medium ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {formatCurrency(item.amountPaid)}
                                </span>
                              </div>
                              <div>
                                {/* <span>
                      {formatCurrency(item.amountPaid)}
                      </span> */}

                                {item?.partPaymentAllowed ? (
                                  <div>
                                    <span
                                      className={`currency-symbol ${
                                        isOverdue
                                          ? "due-date-pass-text fst-italic"
                                          : ""
                                      }`}
                                    >
                                      ₹
                                    </span>
                                    <input
                                      type="number"
                                      className={`form-control input-no-spinner ${
                                        isOverdue
                                          ? "due-date-pass-text fst-italic"
                                          : ""
                                      }`}
                                      value={
                                        editedPayments[item.id] !== undefined
                                          ? editedPayments[item.id]
                                          : item.amountPending
                                      }
                                      min={0}
                                      max={item.amountPending}
                                      readOnly={!item.partPaymentAllowed}
                                      onChange={(e) => {
                                        const value = parseFloat(
                                          e.target.value
                                        );
                                        if (
                                          !isNaN(value) &&
                                          value >= 0 &&
                                          value <= item.amountPending
                                        ) {
                                          setEditedPayments((prev) => ({
                                            ...prev,
                                            [item.id]: value,
                                          }));
                                        }
                                      }}
                                    />
                                  </div>
                                ) : (
                                  <span
                                    className={`fw-medium ${
                                      isOverdue
                                        ? "due-date-pass-text fst-italic"
                                        : ""
                                    }`}
                                  >
                                    {formatCurrency(item.amountPending)}
                                  </span>
                                )}
                              </div>
                              <div>
                                <div>
                                  <i>
                                    
                                  </i>
                                  <small>
                                    {item.partPaymentAllowed
                                      ? "Partial Payment Allowed"
                                      : "Partial Payment Not Allowed"}
                                  </small>
                                </div>
                              </div>
                            </div>
                          );
                        })}

                        {/* Total Row */}
                        <div>
                          <div>
                            <span>Total</span>
                          </div>
                          <div>
                            <span>
                              {formatCurrency(ref.totalAmountToBePaid)}
                            </span>
                          </div>
                          <div></div>
                          <div></div>
                          <div>
                            <span>
                              {formatCurrency(
                                ref.paymentCollectionItems.reduce((sum, p) => {
                                  const paid =
                                    editedPayments[p.id] !== undefined
                                      ? editedPayments[p.id]
                                      : p.amountPending;
                                  return sum + paid;
                                }, 0)
                              )}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Mobile Card View */}
                    <div>
                      {ref.paymentCollectionItems.map((item) => {
                        const isOverdue =
                          new Date(item.dueDate.slice(0, 10)).getTime() <
                          new Date(new Date().setHours(0, 0, 0, 0)).getTime();

                        return (
                          <div key={item.id}>
                            <div>
                              <span>
                                Fees
                              </span>
                              <span>
                                Original Due Amount
                              </span>
                            </div>

                            <div>
                              <div>
                                <span
                                  className={`mobile-value mobile-card-value ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {item.feeType.name}
                                </span>
                                <span
                                  className={`mobile-due-amount mobile-card-value ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {formatCurrency(item.amountToBePaid)}
                                </span>
                              </div>

                              <div>
                                <span>
                                  Paid Amount
                                </span>
                                <span>
                                  Due Date
                                </span>
                              </div>
                              <div>
                                <span
                                  className={`mobile-value mobile-card-value ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {formatCurrency(item.amountPaid)}
                                </span>
                                <span
                                  className={`mobile-value mobile-card-value ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {item.dueDate}
                                </span>
                              </div>

                              <div>
                                <span>
                                  Late Fee Amount
                                </span>
                                <span>
                                  Total Amount Due
                                </span>
                              </div>
                              <div>
                                <span
                                  className={`mobile-value mobile-card-value ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {formatCurrency(item.lateAmountToBePaid)}
                                </span>
                                <span
                                  className={`mobile-value mobile-card-value ${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {formatCurrency(item.amountPending)}
                                </span>
                              </div>
                            </div>

                            <div>
                              {item?.partPaymentAllowed ? (
                                <div>
                                  <span
                                    className={`currency-symbol ${
                                      isOverdue
                                        ? "due-date-pass-text fst-italic"
                                        : ""
                                    }`}
                                  >
                                    ₹
                                  </span>
                                  <input
                                    type="number"
                                    className={`form-control input-no-spinner ${
                                      isOverdue
                                        ? "due-date-pass-text fst-italic"
                                        : ""
                                    }`}
                                    value={
                                      editedPayments[item.id] !== undefined
                                        ? editedPayments[item.id]
                                        : item.amountPending
                                    }
                                    min={0}
                                    max={item.amountPending}
                                    readOnly={!item.amountPending}
                                    onChange={(e) => {
                                      const value = parseFloat(e.target.value);
                                      if (
                                        !isNaN(value) &&
                                        value >= 0 &&
                                        value <= item.amountPending
                                      ) {
                                        setEditedPayments((prev) => ({
                                          ...prev,
                                          [item.id]: value,
                                        }));
                                      }
                                    }}
                                  />
                                </div>
                              ) : (
                                <span
                                  className={`${
                                    isOverdue
                                      ? "due-date-pass-text fst-italic"
                                      : ""
                                  }`}
                                >
                                  {formatCurrency(item.amountPending)}
                                </span>
                              )}
                            </div>

                            <div>
                              <i>
                                
                              </i>
                              <span>
                                {item.partPaymentAllowed
                                  ? "Partial Payment Allowed"
                                  : "Partial Payment Not Allowed"}
                              </span>
                            </div>

                            <div>
                              <span>Total Amount: </span>
                              <span>
                                {formatCurrency(
                                  ref.paymentCollectionItems.reduce(
                                    (sum, p) => {
                                      const paid =
                                        editedPayments[p.id] !== undefined
                                          ? editedPayments[p.id]
                                          : p.amountPending;
                                      return sum + paid;
                                    },
                                    0
                                  )
                                )}
                              </span>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            ))
        )}

        {hasDuePayments && (
          <div>
            <span>
              Total Payment Due: ₹{initialTotalAmount.toLocaleString()}
            </span>
            <span>
              Current Total Paying Amount: ₹{totalAmount.toLocaleString()}
            </span>
          </div>
        )}

        {/* Make Payment Button */}

        {hasDuePayments && (
          <div>
            <div>
              <button
               
                onClick={handleMakePayment}
                disabled={isMakePaymentDisabled}
              >
                Make a Payment
              </button>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

```
</details>

You can follow a similar pattern for the `Payment History`, `Transactions Details`, and `Cancelled Payments` tabs, fetching and displaying the relevant data for each.

### Payment History
This tab shows a complete history of all payment attempts made by the parent, including successful, failed, and pending transactions. This provides a comprehensive audit trail.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/sp-cash.png)

> **Tip**
> You can even download the payment history, by clicking on Payment History Btn as shown above.

Downloaded Payment History 

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/stu-8.png)
<details>
<summary>Complete Source Code for Payment Screen Tab Component</summary>

```jsx
"use client";

import {
  ClosedArrowIcon,
  OpenArrowIcon,
  PaymentHistoryPaidIcon,
} from "@/utils/App-icons";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useLazyGetStudentPaymentRecordQuery } from "@/store/services/studentApi"; // adjust if path differs
import { setStudentPayments } from "@/store/slices/studentPaymentSlice";
import { RootState } from "@/store";
import axios from "axios";

interface PaymentCollectionItem {
  id: number;
  amountPaid: number;
  amountPending: number;
  amountToBePaid: number;
  dueDate: string;
  isOverdue: boolean;
  lateAmountToBePaid: number;
  partPaymentAllowed: boolean;
  status: string;
  feeType: {
    id: number;
    name: string;
  };
  mode:string;
}

interface StudentPaymentRecord {
  id: number;
  name: string;
  description: string;
  createdOn: string;
  totalAmountToBePaid: number;
  institute: {
    id: number;
    name: string;
  };
  paymentCollectionItems: PaymentCollectionItem[];
}

export default function PaymentHistoryPage() {
  const dispatch = useDispatch();
  const student = useSelector((state: RootState) => state.student.data);
  const studentPayments = useSelector(
    (state: RootState) => state.studentPayments.data
  );
  const [fetchPayments] = useLazyGetStudentPaymentRecordQuery();
  const [expandedRefs, setExpandedRefs] = useState<number[]>([]);

  useEffect(() => {
    if (student?.studentLoginId) {
      fetchPayments({ studentLoginId: student.studentLoginId, isPaid: true }).then(
        (res) => {
          if (res?.data?.data) {
            dispatch(setStudentPayments(res.data.data));
            const defaultExpandedIds = res.data.data.map(
              (d: StudentPaymentRecord) => d.id
            );
            setExpandedRefs(defaultExpandedIds);
          }
        }
      );
    }
  }, [student?.studentLoginId]);

  const toggleRef = (refId: number) => {
    setExpandedRefs((prev) =>
      prev.includes(refId)
        ? prev.filter((ref) => ref !== refId)
        : [...prev, refId]
    );
  };
  const formatCurrency = (amount: number) => {
    return `₹${amount.toLocaleString()}`;
  };

  const downloadStudentFeeReport = async () => {
    if (!student?.studentLoginId) return;

    try {
      const token = localStorage.getItem("token") || "";
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_API_URL}/api/payment/download-student-fee-report?studentLoginId=${student.studentLoginId}`,
        {},
        {
          responseType: "blob", // ✅ goes here
          headers: {
            Authorization: `Bearer ${token}`, // ✅ now properly sent
            "Content-Type": "application/json",
          },
        }
      );

      const disposition = response.headers["content-disposition"];
      const filename =
        disposition?.split("filename=")[1]?.replace(/"/g, "") ||
        `payment-history-${Date.now()}.xlsx`;

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();

      // Optional toast
    } catch (error) {
      console.error("Download error:", error);
    }
  };

  const isAllPaymentItemsEmpty = studentPayments?.every(
    (payment) => payment.paymentCollectionItems.length === 0
  );

  return (
    <div>
      {/* Payment History Header */}
      <div>
        <div>
          Payment History
        </div>
      </div>
      <div>
        <button
         
          onClick={downloadStudentFeeReport}
          disabled={!studentPayments || isAllPaymentItemsEmpty}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            fill="currentColor"
           
            viewBox="0 0 16 16"
          >
            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5" />
            <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708z" />
          </svg>
          Payment History
        </button>
      </div>

      {/* Payment References */}

      {studentPayments &&
      studentPayments.filter(
        (ref) =>
          ref.paymentCollectionItems?.length > 0 
        && ref.paymentCollectionItems.every((item) => item.status === 'Fully Paid' || item.status === 'Partially Paid')
      ).length === 0 ? (
        <p>
          No Payment History Available
        </p>
      ) : (
        studentPayments
          ?.filter(
            (ref) =>
              ref.paymentCollectionItems?.length > 0 &&
              ref.paymentCollectionItems.every(
                (item) => item.status === 'Fully Paid' || item.status === 'Partially Paid'
              )
          )
          ?.map((ref) => (
            <div key={ref.id}>
              {/* Reference Header */}
              <div
               
                onClick={() => toggleRef(ref.id)}
              >
                <div>
                  <div>
                    {expandedRefs.includes(ref.id) ? (
                      
                    ) : (
                      
                    )}
                    <span>
                      <span>
                        {ref.name}
                      </span>
                    </span>
                  </div>
                  <div>
                    <small>
                      Created On:{" "}
                      <span>
                        {ref.createdOn}
                      </span>
                    </small>
                  </div>
                </div>
              </div>

              {/* Reference Content */}
              {expandedRefs.includes(ref.id) && (
                <div className={`payment-ref-content`}>
                  {ref?.paymentCollectionItems?.length === 0 ? (
                    <p>
                      No Payment History Available
                    </p>
                  ) : (
                    <>
                      {/* Desktop Table View */}
                      <div>
                        <div>
                          <div>
                            Fees
                          </div>
                          <div>
                            Due Amount
                          </div>
                          <div>
                            Due Date
                          </div>
                          <div>
                            Late Fee Amount
                          </div>
                          <div>
                            Paid Amount
                          </div>
                          <div>
                            Mode
                          </div>
                          <div>
                            Status
                          </div>
                        </div>

                        {ref.paymentCollectionItems.map((item) => (
                          <div key={item.id}>
                            <div>
                              <span>
                                {item.feeType.name}
                              </span>
                            </div>
                            <div>
                              <span>{formatCurrency(item.amountToBePaid)}</span>
                            </div>
                            <div>
                              <span>{item.dueDate}</span>
                            </div>
                            <div>
                              <span>
                                {formatCurrency(item.lateAmountToBePaid)}
                              </span>
                            </div>
                            <div>
                              <span>{formatCurrency(item.amountPaid)}</span>
                            </div>
                            <div>
                              <span className={`payment-chip ${item.mode?.toLowerCase()}`}>
                                {item.mode}
                              </span>
                            </div>
                            <div>
                              <div>
                                <i>
                                  
                                </i>
                                <small>
                                  {item.status}
                                </small>
                              </div>
                            </div>
                          </div>
                        ))}

                        <div>
                          <div>
                            <span>Total</span>
                          </div>
                          <div>
                            <span>
                              {formatCurrency(ref.totalAmountToBePaid)}
                            </span>
                          </div>
                          <div></div>
                          <div></div>
                          <div>
                          <span>
                              {formatCurrency(
                                ref.paymentCollectionItems.reduce(
                                  (sum, p) => sum + p.amountPaid,
                                  0
                                )
                              )}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Mobile View */}
                      <div>
                        {ref.paymentCollectionItems.map((item) => (
                          <div key={item.id}>
                            <div>
                              <span>
                                Fees
                              </span>
                              <span>
                                Due Amount
                              </span>
                            </div>

                            <div>
                              <div>
                                <span>
                                  {item.feeType.name}
                                </span>
                                <span>
                                  {formatCurrency(item.amountToBePaid)}
                                </span>
                              </div>

                              <div>
                                <span>
                                  Late Fee Amount
                                </span>
                                <span>
                                  Paid Amount
                                </span>
                              </div>
                              <div>
                                <span>
                                  {formatCurrency(item.lateAmountToBePaid)}
                                </span>
                                <span>
                                  {formatCurrency(item.amountPaid)}
                                </span>
                              </div>

                              <div>
                                <span>
                                  Due Date
                                </span>
                              </div>
                              <div>
                                <span>
                                  {item.dueDate}
                                </span>
                              </div>
                               <div>
                                <span>
                                  Mode
                                </span>
                              </div>
                              <div>
                              <span className={`payment-chip ${item.mode?.toLowerCase()}`}>
                                {item.mode}
                              </span>
                              </div>
                            </div>

                            <div>
                              <i>
                                
                              </i>
                              <span>{item.status}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          ))
      )}
    </div>
  );
}

```
</details>

###  Transactions Details
This tab provides a view of all transactions associated with the student, which can be useful for reconciliation purposes.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/transaction-details.png)
<details>
<summary>Complete Source Code for Transaction Details Tab Component</summary>

```jsx
"use client";

import { ClosedArrowIcon, OpenArrowIcon } from "@/utils/App-icons";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useLazyGetStudentPaymentTransactionRecordQuery } from "@/store/services/studentApi"; // adjust if path differs
import { RootState } from "@/store";
import { setStudentPaymentTransactions } from "@/store/slices/studentPaymentTransactionSlice";

interface PaymentCollectionItem {
  id: number;
  amountPaid: number;
  amountPending: number;
  amountToBePaid: number;
  dueDate: string;
  isOverdue: boolean;
  lateAmountToBePaid: number;
  partPaymentAllowed: boolean;
  status: string;
  feeType: {
    id: number;
    name: string;
  };
}

interface StudentPaymentRecord {
  id: number;
  name: string;
  description: string;
  createdOn: string;
  totalAmountToBePaid: number;
  institute: {
    id: number;
    name: string;
  };
  paymentCollectionItems: PaymentCollectionItem[];
}

export default function PaymentsPage() {
  const dispatch = useDispatch();
  const student = useSelector((state: RootState) => state.student.data);
  const studentPaymentTransactions = useSelector(
    (state: RootState) => state.studentPaymentTransactions.data
  );
  const [fetchPayments] = useLazyGetStudentPaymentTransactionRecordQuery();
  // const [expandedRefs, setExpandedRefs] = useState<string[]>(["02"]);
  const [expandedRefs, setExpandedRefs] = useState<number[]>([]);

  useEffect(() => {
    if (student?.studentLoginId) {
      fetchPayments({ studentLoginId: student.studentLoginId}).then((res) => {
        if (res?.data?.data) {
          dispatch(setStudentPaymentTransactions(res.data.data));
          const defaultExpandedIds = res?.data?.data?.map(
            (d: StudentPaymentRecord) => d?.id
          );
          setExpandedRefs(defaultExpandedIds);
        }
      });
    }
  }, [student?.studentLoginId]);

  const toggleRef = (refId: number) => {
    setExpandedRefs((prev) =>
      prev.includes(refId)
        ? prev.filter((ref) => ref !== refId)
        : [...prev, refId]
    );
  };
  const formatCurrency = (amount: number) => {
    return `₹${amount.toLocaleString()}`;
  };

  return (
    <div>
      {/* Payment History Header */}
      <div>
        <div>
          Payments Details
        </div>
      </div>
      {/* Payment References */}
      {studentPaymentTransactions?.length === 0 ||
      !studentPaymentTransactions ? (
        <p>
          {" "}
          No Payment Details Available
        </p>
      ) : (
        studentPaymentTransactions?.map((ref) => (
          <div key={ref.id}>
            {/* Reference Header */}
            <div
             
              onClick={() => toggleRef(ref.id)}
            >
              <div>
                <div>
                  {/*  */}
                  {expandedRefs.includes(ref.id) ? (
                    
                  ) : (
                    
                  )}
                  <span>
                    {" "}
                    <span>{ref.id}</span>
                  </span>
                </div>
                <div>
                  <small>
                    Created On:{" "}
                    <span>
                      {ref.createdAt.slice(0, 10)}
                    </span>
                  </small>
                </div>
              </div>
            </div>

            {/* Reference Content */}
            {expandedRefs.includes(ref.id) && (
              <div>
                {/* Desktop Table View */}
                <div>
                  {/* Table Header */}
                  <div>
                    <div>
                      Order Id
                    </div>
                    <div>
                      Transaction Id
                    </div>
                    <div>
                      Amount
                    </div>
                    <div>
                      Payment Status
                    </div>
                  </div>

                  {/* Payment Rows */}
                  {/* {ref.map((item) => ( */}
                  <div key={ref.id}>
                    <div>
                      <span>{ref.mSwipeIpgOrderId}</span>
                    </div>
                    <div>
                      <span>{ref.mSwipeIpgTransId}</span>
                    </div>
                    {/* <div>
                        <span>{ref.mSwipeIpgInvoiceId}</span>
                      </div> */}
                    <div>
                      <span>{ref.amount}</span>
                    </div>
                    <div>
                      <div>
                        <small>
                          {ref.paymentStatus}
                        </small>
                      </div>
                    </div>
                  </div>
                  {/* // ))} */}

                  {/* Total Row */}
                  {/* <div>
                    <div>
                      <span>Total</span>
                    </div>
                    <div>
                      <span>
                        {" "}
                        {formatCurrency(ref.totalAmountToBePaid)}
                      </span>
                    </div>
                    <div>
                      <span></span>
                    </div>
                    <div>
                      <span>
                        {formatCurrency(
                          ref.paymentCollectionItems.reduce(
                            (sum, p) => sum + p.amountPaid,
                            0
                          )
                        )}
                      </span>
                    </div>
                    <div>
                      <div></div>
                    </div>
                  </div> */}
                </div>

                {/* Mobile Card View */}
                <div>
                  {/* {ref.paymentCollectionItems.map((item) => ( */}
                  <div key={ref.id}>
                    <div>
                      <span>
                        Order Id
                      </span>
                      <span>
                        Transaction Id
                      </span>
                    </div>

                    <div>
                      <div>
                        <span>
                          {ref.mSwipeIpgOrderId}
                        </span>
                        <span>
                          {ref.mSwipeIpgTransId}
                        </span>
                      </div>

                      <div>
                        <span>
                          Transaction Id
                        </span>
                        <span>
                          Amount
                        </span>
                      </div>
                      <div>
                        <span>
                          {ref.mSwipeIpgTransId}
                        </span>
                        <span>
                          {formatCurrency(ref.amount)}
                        </span>
                      </div>
                    </div>

                    <div>
                      <span>{ref.paymentStatus}</span>
                    </div>
                  </div>
                  {/* ))} */}
                </div>
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
}

```
</details>

### Cancelled Payments
This tab lists any payments that were initiated but subsequently cancelled either by the user or the system.

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/sp-cancel.png)
<details>
<summary>Complete Source Code for Cancelled Tab Component</summary>

```jsx
"use client";

import { ClosedArrowIcon, OpenArrowIcon } from "@/utils/App-icons";
import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useLazyGetStudentPaymentCancelRecordQuery } from "@/store/services/studentApi"; // adjust if path differs
import { RootState } from "@/store";
import { setStudentCancelPayment } from "@/store/slices/studentCancelPaymentSlice";

interface StudentCancelPayment {
  id: number;
  status: string;
  createdAt: string;
  amountToBePaid: number;
  amountPaid: number;
  institute: {
    id: number;
    name: string;
  };
  feeType: {
    feeType: string
  }
  paymentCollection: {
    name: string;
  }
  dueDate: string;
  mode?: string;
}

export default function CancelledPaymentPage() {
  const dispatch = useDispatch();
  const student = useSelector((state: RootState) => state.student.data);
  const StudentCancelPayment = useSelector(
    (state: RootState) => state.studentCancelPayment.data
  );
  const [getStudentPaymentCancelRecord] = useLazyGetStudentPaymentCancelRecordQuery();
  // const [expandedRefs, setExpandedRefs] = useState<string[]>(["02"]);
  const [expandedRefs, setExpandedRefs] = useState<string[]>([]);

  useEffect(() => {
    if (student?.studentLoginId) {
      getStudentPaymentCancelRecord({ studentLoginId: student.studentLoginId }).then((res) => {
        if (res?.data?.data) {
          dispatch(setStudentCancelPayment(res.data.data));
          const defaultExpandedIds = res?.data?.data?.map(
            (d: StudentCancelPayment) => d?.paymentCollection?.name || ""
          );
          setExpandedRefs(defaultExpandedIds);
        }
      });
    }
  }, []);

  const toggleRef = (key: string) => {
    setExpandedRefs((prev) =>
      prev.includes(key)
        ? prev.filter((k) => k !== key)
        : [...prev, key]
    );
  };

  const formatCurrency = (amount: number) => {
    return `₹${amount.toLocaleString()}`;
  };

  const uniqueStudentCancelPayment = Array.from(
    new Map(
      StudentCancelPayment?.map((item) => [item.id, item])
    ).values()
  );

  const groupedByCollection = uniqueStudentCancelPayment?.reduce(
    (acc: Record<string, StudentCancelPayment[]>, item) => {
      const key = item.paymentCollection?.name || "Unknown Collection";
      if (!acc[key]) acc[key] = [];
      acc[key].push(item);
      return acc;
    },
    {}
  ) || {};

  return (
    <div>
      {/* Payment History Header */}
      <div>
        <div>
          Cancelled Payments
        </div>
      </div>
      {/* Payment References */}
      {StudentCancelPayment?.length === 0 ||
        !StudentCancelPayment ? (
        <p>
          {" "}
          No Cancelled Payments Available
        </p>
      ) : (
        
          Object.entries(groupedByCollection).map(([collectionName, records]) => (
            <div key={collectionName}>

              {/* Group Header */}
              <div
               
                onClick={() => toggleRef(collectionName)}
              >
                <div>
                  <div>
                    {/*  */}
                    {expandedRefs.includes(collectionName) ? (
                      
                    ) : (
                      
                    )}
                    <span>
                      {" "}
                      <span>
                        {collectionName}
                      </span>
                    </span>
                  </div>
                  <div>
                    <small>
                      Created On: {"  "}
                      <span>
                        {records[0].createdAt.slice(0, 10)}
                      </span>
                    </small>
                  </div>
                </div>
              </div>

              {/* Group Records */}
              {expandedRefs.includes(collectionName) && (
                <div>
                  {/* Desktop Table View */}
                  <div>
                    <div>
                      <div>Fees</div>
                      <div>Due Date</div>
                      <div>Amount </div>
                      <div>Mode</div>
                      <div>Status</div>
                    </div>

                    {records.map((ref) => (
                      <div key={ref.id}>
                        <div>{ref.feeType?.feeType}</div>
                        <div>{ref.dueDate}</div>
                        <div>{formatCurrency(ref.amountToBePaid)}</div>
                       
                          <div>
                              <span className={`payment-chip ${ref.mode?.toLowerCase()}`}>
                                {ref.mode}
                              </span>
                            </div>
                        <div>{ref.status}</div>
                      </div>
                    ))}
                  </div>

                  {/* Mobile Card View */}
                  <div>
                    {records.map((ref) => (
                      <div key={ref.id}>
                        <div>
                          <div>
                            <span>Fees</span>
                            <span>{ref.feeType?.feeType}</span>
                          </div>
                          <div>
                            <span>Amount</span>
                            <span>{formatCurrency(ref.amountToBePaid)}</span>
                          </div>
                          <div>
                            <span>Status</span>
                            <span>{ref.status}</span>
                          </div>
                          <div>
                            <span>Created On</span>
                            <span>{ref.createdAt?.slice(0, 10)}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                </div>
              )}

            </div>
          ))
        
      )}
    </div>
  );
}

```
</details>

## Profile Management

The profile page allows parents to view and update their personal and contact information.

-   **URL**: `/dashboard/profile`
-   **Editable Fields**:
    -   First Name
    -   Last Name
    -   Parent's Email Address (for notifications)
    -   Mobile Number

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/stu-7.png)

Here's an example of how you can structure the profile page at `src/app/dashboard/profile/page.tsx`:
<details>
<summary>Complete Source Code for Profile Component</summary>

```jsx
"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowIcon } from "@/utils/App-icons";
import { useProtectedRoute } from "@/hooks/useProtectedRoute";
import {
  useLazyGetStudentQuery,
  useUpdateStudentMutation,
} from "@/store/services/studentApi";
import { showToast } from "@/store/slices/toastSlice";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { RootState } from "@/store/index";
import { setStudent } from "@/store/slices/studentSlice";

export default function ProfilePage() {
  const student = useSelector((state: RootState) => state.student.data);
  const dispatch = useDispatch();
  const [updateStudent] = useUpdateStudentMutation();
  const [getStudent] = useLazyGetStudentQuery();
  const [studentData, setStudentData] = useState({
    studentLoginId: "",
    studentName: "",
    parentName: "",
    parentEmailAddress: "",
    studentMobileNumber: "",
  });

  const [isModified, setIsModified] = useState(false);

  const { isAllowed, loading } = useProtectedRoute();

  useEffect(() => {
    const id = localStorage.getItem("id");
    if (!student && id) {
      getStudent({ id }).then((res) => {
        if (res?.data) {
          dispatch(setStudent(res.data?.data));
        }
      });
    }
  }, [student, getStudent, dispatch]);

  // 🔄 Update form state from Redux student
  useEffect(() => {
    if (student) {
      setStudentData({
        studentLoginId: student?.studentLoginId,
        studentName: student.studentName || "",
        parentName: student.parentName || "",
        parentEmailAddress: student.parentEmailAddress || "",
        studentMobileNumber: student.studentMobileNumber || "",
      });
    }
  }, [student]);

  // ✅ Do this AFTER all hooks
  if (loading) return null;
  if (!isAllowed) return null;

  const handleInputChange = (field: string, value: string) => {
    setStudentData((prev) => ({ ...prev, [field]: value }));
    setIsModified(true);
  };

  const handleSaveChanges = async () => {
    try {
      const id = localStorage.getItem("id");
      const res = await updateStudent({ id, studentData }).unwrap();
      if (res?.statusCode === 200) {
        dispatch(setStudent(res?.data));
        dispatch(
          showToast({
            severity: "success",
            summary: "",
            detail: "Profile Update Successfully.",
          })
        );
        setIsModified(false);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      {/* Page Header */}
      <div>
        <div>
          My Profile

          {/* Breadcrumb Navigation */}
          <nav aria-label="breadcrumb">
            <ol>
              <li>
                <Link
                  href="/dashboard"
                 
                >
                  Home
                </Link>
              </li>
              <li>
                <div>
                  
                </div>
              </li>
              <li
               
                aria-current="page"
              >
                Profile
              </li>
            </ol>
          </nav>
        </div>
      </div>

      {/* Profile Form */}
      <div>
        <div>
          <div>
            <div>
              {/* Student ID */}
              <div>
                <div>
                  <label>
                    Student ID
                  </label>
                  <input
                    type="text"
                   
                    value={studentData?.studentLoginId}
                    disabled
                    style={{
                      backgroundColor: "#f8f9fa",
                      borderColor: "#e9ecef",
                      color: "#6c757d",
                    }}
                  />
                </div>
              </div>

              {/* Name Fields */}
              <div>
                <div>
                  <label>
                    First Name
                  </label>
                  <input
                    type="text"
                   
                    value={studentData?.studentName}
                    onChange={(e) =>
                      handleInputChange("studentName", e.target.value)
                    }
                    style={{
                      borderColor: "#e9ecef",
                    }}
                  />
                </div>
                <div>
                  <label>
                    Last Name
                  </label>
                  <input
                    type="text"
                   
                    value={studentData?.parentName}
                    onChange={(e) =>
                      handleInputChange("parentName", e.target.value)
                    }
                    style={{
                      borderColor: "#e9ecef",
                    }}
                  />
                </div>
              </div>

              {/* Contact Fields */}
              <div>
                <div>
                  <label>
                    Parent Email Address
                  </label>
                  <input
                    type="parentEmailAddress"
                   
                    value={studentData?.parentEmailAddress}
                    onChange={(e) =>
                      handleInputChange("parentEmailAddress", e.target.value)
                    }
                    style={{
                      borderColor: "#e9ecef",
                    }}
                  />
                </div>
                <div>
                  <label>
                    Phone Number
                  </label>
                  <input
                    type="tel"
                   
                    value={studentData?.studentMobileNumber}
                    onChange={(e) =>
                      handleInputChange("studentMobileNumber", e.target.value)
                    }
                    style={{
                      borderColor: "#e9ecef",
                    }}
                  />
                </div>
              </div>

              {/* Save Button */}
              <div>
                <button
                 
                  onClick={handleSaveChanges}
                  disabled={!isModified}
                  style={{
                    backgroundColor: isModified ? "#0d6efd" : "#6c757d",
                    borderColor: isModified ? "#0d6efd" : "#6c757d",
                  }}
                >
                  Save Changes
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

```
</details>

# Student API Endpoints

## Base Configuration
```typescript
baseUrl: process.env.NEXT_PUBLIC_BACKEND_API_URL
Authorization: Bearer {token} // Stored in localStorage
```

## Endpoints

### Authentication

| Method | Endpoint | Hook | Description |
|--------|----------|------|-------------|
| `GET` | `/api/student/login/initiate/{studentLoginId}` | `useLazyValidateStudentQuery()` | Validate student exists |
| `POST` | `/api/student/initiate-otp` | `useInitiateOtpMutation()` | Send OTP to student |
| `POST` | `/api/student/verify-otp` | `useVerifyOtpMutation()` | Verify OTP and get token |

**Body Examples:**
```typescript
// Initiate OTP
{ studentLoginId: "STUDENT123" }

// Verify OTP
{ studentLoginId: "STUDENT123", otp: "123456" }
```

### Student Records

| Method | Endpoint | Hook | Description |
|--------|----------|------|-------------|
| `GET` | `/api/student/get-student-record?id={id}` | `useLazyGetStudentQuery()` | Get student details |
| `PATCH` | `/api/student/update-student-record?id={id}` | `useUpdateStudentMutation()` | Update student record |
| `GET` | `/api/student/get-institute-record?userId={userId}` | `useLazyGetInstituteRecordQuery()` | Get institute details |

**Body Example (Update):**
```typescript
{ id: "123", studentData: { name: "John", phone: "+123" } }
```

### Institute Records

| Method | Endpoint | Hook | Description |
|--------|----------|------|-------------|
| `GET` | `/api/student/get-institute-record?userId={userId}` | `useLazyGetInstituteRecordQuery()` | Get institute details |

### Payments

| Method | Endpoint | Hook | Description |
|--------|----------|------|-------------|
| `GET` | `/api/payment?studentLoginId={studentLoginId}&status={status}` | `useLazyGetStudentPaymentsQuery()` | Get payments by status |
| `GET` | `/api/payment-collection/student-payment-summary?studentLoginId={studentLoginId}&isPaid={isPaid}` | `useLazyGetStudentPaymentRecordQuery()` | Get payment summary |
| `POST` | `/api/payment/payment-gateway` | `usePaymentGatwayMutation()` | Initiate payment gateway |
| `GET` | `/api/payment/payment-transaction-history?studentLoginId={studentLoginId}` | `useLazyGetStudentPaymentTransactionRecordQuery()` | Get transaction history |
| `GET` | `/api/payment-collection-item/payment-cancel-record?studentLoginId={studentLoginId}` | `useLazyGetStudentPaymentCancelRecordQuery()` | Get cancelled payments |

**Body Example (Payment Gateway):**
```typescript
{
  studentLoginId: "STUDENT123",
  amountMap: { "fee1": 1000, "fee2": 2000 },
  totalAmount: 3000
}
```

## Quick Reference
```typescript
import {
  useLazyValidateStudentQuery,
  useInitiateOtpMutation,
  useVerifyOtpMutation,
  useLazyGetStudentPaymentsQuery,
  useUpdateStudentMutation,
  useLazyGetStudentQuery,
  useLazyGetInstituteRecordQuery,
  useLazyGetStudentPaymentRecordQuery,
  usePaymentGatwayMutation,
  useLazyGetStudentPaymentTransactionRecordQuery,
  useLazyGetStudentPaymentCancelRecordQuery
} from '@/store/services/studentApi';
```

## Usage Pattern
```typescript
// Query (GET)
const [trigger, { data, isLoading, error }] = useLazyGetStudentQuery();
await trigger({ id: '123' });

// Mutation (POST/PATCH)
const [mutate, { isLoading }] = useUpdateStudentMutation();
await mutate({ id: '123', studentData: {...} }).unwrap();
```

## Other Pages

The portal also includes standard static pages, which can be customized.

-   `/privacyPolicy`: To display the institute's privacy policy.
-   `/faq`: For frequently asked questions about the fee payment process.
-   `/termsandcondition`: To display the institute's terms and conditions.

These pages are essential for providing comprehensive information and support to the users.
