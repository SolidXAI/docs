---
sidebar_position: 2
---

# Institute User Workflows

This section covers the primary workflows for an institute's administrative user, from logging in to managing payments.

## User Login and Access Control

An `InstituteUser` is a user who belongs to a specific institute. Their access must be strictly limited to their own institute's data.

### The Magic of Security Record Rules

SolidX achieves this data isolation not by writing complex queries in every service, but by using **Security Record Rules**. These are powerful, metadata-driven rules that automatically filter data for a user based on their role and relationships.

**Example Rule:**

-   **Goal:** An Institute Admin should only see students from their own institute.
-   **Rule Logic:** "For a user with the 'Institute Admin' role, when they query for `Student` records, only return the records where the `Student`'s `institute` field matches the `institute` field of the logged-in user's own `InstituteUser` record."

This is configured once in the **Solid Core > Security > Security Record Rule** section of the admin panel. After that, every query, API call, and list view is automatically and securely filtered, providing robust multi-tenancy out of the box.

![Default Login Page](/img/tutorial/school-fees-portal/5-recipes/security-rule.png)

<!-- ## User Dashboard

Upon logging in, the Institute Admin should be greeted with a dashboard providing an at-a-glance view of the institute's financial health.

:::tip
Dashboard feature will come shortly.
:::

### Key Metrics on the Dashboard

-   **Total Collected:** A sum of all successful payments for the current academic year.
-   **Total Outstanding:** The total amount pending from all students.
-   **Total Overdue:** The portion of the outstanding amount that is past its due date.
-   **Recent Transactions:** A list of the 5-10 most recent payment activities (successful or failed).
-   **Quick Actions:** Buttons to "Start a New Payment Collection" or "View All Students".




``` -->

## Institute User — Create / Download Excel for Upload

Once the institute is onboarded and fee types are configured, the Institute Admin can upload student fee mappings in bulk.
To simplify this, the system provides a Sample Excel Template that the admin can download, fill, and re-upload.

### How It Works

The Institute Admin navigates to:
Fees Portal → Initiate Payment

A button Download Sample Excel is shown.

Clicking this button downloads an auto-generated Excel file with pre-defined headers.

The admin can now add or edit any number of rows, following the structure provided.

:::tip Easy Bulk Upload
The sample Excel ensures every institute follows a consistent data structure, reducing upload errors and making large student lists easy to import.
:::

### Excel Template Structure

| Column Name           | Description                                                           |
| --------------------- | --------------------------------------------------------------------- |
| **Student ID**        | Unique identifier per institute (composite index ensures uniqueness). |
| **Student Name**      | Name of the student.                                                  |
| **Parent Name**       | Parent or guardian name.                                              |
| **Parent Email**      | Email used for sending payment links & reminders.                     |
| **Fee Types**         | One or multiple fee types mapped (dynamic per institute).             |
| **Fee Type Due Date** | Due date for each fee type.                                           |
| **Payment Mode**      | PG / Cash                          |

:::info Template Evolution
Fee Types column is dynamic — the system generates columns based on the institute’s configured fee types.
:::

### UI Preview

![Default Login Page](/img/tutorial/school-fees-portal/6-usecase/excel.png)

:::tip Payment Modes
The system supports **two payment modes** — **Payment Gateway (PG)** and **Cash**.

- **PG Mode:** Creates a pending payment record and sends a payment link to the parent.  
- **Cash Mode:** Marks the payment as *Paid* instantly. No reminders, schedulers, or subscribers will process these records since they are already completed.

This ensures accurate tracking while preventing unnecessary notifications for cash-settled payments.
:::


## Institute User — Initiate Payment

When an Institute Admin clicks Initiate Payment, the system automatically creates payment records for all students based on the institute’s configured fee types.

### How It Works (Short Version)
- Dynamic Fee Type Loading
- The system fetches all active fee types for the institute. This makes the process fully dynamic — no manual mapping required.
- Auto-Generate Payment Records

### Using:

- Uploaded student Excel with Configured fee types
- The system generates necessary payment entries (Pending status) for each student–fee type combination.

### Preview

![Default Login Page](/img/tutorial/school-fees-portal/6-usecase/initiate-payment.png)

### Code Snippets

#### Controller Endpoint
The controller receives the uploaded file and initiates the validation and creation process.
```Typescript
  @ApiTags('Fees Portal')
  @Controller('payment-collection')
  export class PaymentCollectionController {
    constructor(private readonly service: PaymentCollectionService) { }

    @ApiBearerAuth('jwt')
    @Post()
    @UseInterceptors(AnyFilesInterceptor())
    async create(
      @Body() createDto: CreatePaymentCollectionDto,
      @UploadedFiles() files: Array<Express.Multer.File>,
    ) {
      await this.service.feeTypeValidation(createDto, files)
      return this.service.create(createDto, files);
    }
  }

```

#### Excel Validation Logic (`feeTypeValidation`)
This function performs a series of validations on the uploaded Excel file before processing the data.

<details>
<summary>Step 1: Read Excel and Validate Fee Types</summary>

```typescript
  //these validates both feetypes as well past due date
  async feeTypeValidation(
    createDto: CreatePaymentCollectionDto,
    files: Express.Multer.File[],
  ) {
    if (!files?.length) {
      throw new BadRequestException('Excel file is required');
    }

    const { instituteId, ...rest } = createDto;

    if (!instituteId) {
      throw new BadRequestException('Institute ID is required');
    }

    const file = files[0];

    // Step 1: Read Excel using ExcelJS
    const workbook = new ExcelJS.Workbook();
    await workbook.xlsx.readFile(file.path); // ✅ load from file path

    const worksheet = workbook.worksheets[0];
    const headerRow = worksheet.getRow(1);

    const headers: string[] = (headerRow.values as ExcelJS.CellValue[])
      .slice(1)
      .filter((cell): cell is string => typeof cell === 'string')
      .map((cell) => cell.trim());

    // Step 2: Define known non-fee fields
    const knownFields = [
      'Student Name',
      'Student Id',
      'Parent / Guardian Name',
      'Parent / Guardian Email',
      'Parent / Guardian Mobile',
      'Payment Mode'
    ];

    // Step 3: Identify fee type columns dynamically
    const possibleFeeTypes = headers
      .filter((header) => {
        const normalized = header.toLowerCase();
        return (
          !knownFields.some((f) => f.toLowerCase() === normalized) &&
          !normalized.includes('due date')
        );
      })
      .map((header) => header.trim());

    const uniqueFeeTypes = Array.from(new Set(possibleFeeTypes)).filter(
      Boolean,
    );

    if (!uniqueFeeTypes.length) {
      throw new BadRequestException('No fee types found in Excel headers.');
    }
```
</details>

<details>
<summary>Step 2: Validate against FeeType Master</summary>

```typescript
    // Step 4: Validate against FeeType master for institute
    const existingFeeTypes = await this.feeTypeRepo
      .createQueryBuilder('fee_type')
      .leftJoin('fee_type.institute', 'institute')
      .where('fee_type.feeType IN (:...names)', { names: uniqueFeeTypes })
      .andWhere('institute.id = :instituteId', { instituteId: instituteId })
      .getMany();

    const existingNames = existingFeeTypes.map((f) => f.feeType);
    const missingFeeTypes = uniqueFeeTypes.filter(
      (name) => !existingNames.includes(name),
    );

    if (missingFeeTypes.length) {
      throw new BadRequestException(
        `These fee types are not configured for the institute: ${missingFeeTypes.join(', ')}`,
      );
    }
```
</details>

<details>
<summary>Step 3: Validate Due Dates</summary>

```typescript
    // Step 5: Validate due dates are not in the past
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Normalize to midnight

    for (let i = 2; i <= worksheet.rowCount; i++) {
      const row = worksheet.getRow(i);
      if (!row.hasValues) continue;

      for (const feeType of uniqueFeeTypes) {
        const dueDateHeader = `${feeType} Due Date`;
        const dueDateIndex = headers.findIndex(h => h === dueDateHeader);
        if (dueDateIndex === -1) continue;

        const dueDateCell = row.getCell(dueDateIndex + 1); // ExcelJS is 1-based
        let dueDateValue: Date | null = null;

        if (typeof dueDateCell.value === 'string' && dueDateCell.value.trim()) {
          // Parse yyyy-mm-dd
          const [year, month, day] = dueDateCell.value.trim().split('-').map(Number);
          dueDateValue = new Date(year, month - 1, day);
        } else if (dueDateCell.type === ExcelJS.ValueType.Date && dueDateCell.value instanceof Date) {
          dueDateValue = dueDateCell.value;
        }
        if (dueDateValue && dueDateValue < today) {
          throw new BadRequestException(
            `Invalid due date: The entered due date (${dueDateCell.value}) is earlier than today's date. 
            Past due dates are not allowed. 
            Please provide a valid due date (today or a future date) for student "${row.getCell(headers.indexOf('Student Name') + 1).value}" and fee type "${feeType}".`
          );
        }
      }
    }
```
</details>

<details>
<summary>Step 4: Validate Payment Mode</summary>

```typescript
    // Step 6: Validate Payment Mode
    const paymentModeIndex = headers.findIndex(
      (h) => h.toLowerCase() === 'payment mode'.toLowerCase(),
    );

    if (paymentModeIndex !== -1) {
      for (let i = 2; i <= worksheet.rowCount; i++) {
        const row = worksheet.getRow(i);
        if (!row.hasValues) continue;

        const cell = row.getCell(paymentModeIndex + 1);
        let value = (cell.value || '').toString().trim().toUpperCase();

        // Default to PG if empty
        if (!value) {
          value = 'PG';
          cell.value = 'PG'; // optional: normalize the sheet value
        }

        if (value !== 'CASH' && value !== 'PG') {
          throw new BadRequestException(
            `Invalid Payment Mode "${cell.value}" found for student "${row.getCell(
              headers.indexOf('Student Name') + 1,
            ).value}". Only "CASH" or "PG" are allowed. If empty, default is "PG".`,
          );
        }
      }
    } else {
      throw new BadRequestException(
        'Payment Mode column is missing in Excel file.',
      );
    }
```
</details>

<details>
<summary>Step 5: Validate Email Format</summary>

```typescript
    //add validation : parent and student email value should be in lowarcase and both are mandatory
    const getEmailValue = (cell: ExcelJS.Cell): string => {
      if (!cell.value) return '';

      if (typeof cell.value === 'string') return cell.value.trim();

      if (typeof cell.value === 'object' && 'text' in cell.value) {
        return (cell.value as any).text.trim(); // ✅ use text property
      }

      return String(cell.value).trim();
    };
    //
    const parentEmailIndex = headers.findIndex(
      (h) => h.toLowerCase() === 'parent / guardian email'.toLowerCase(),
    );
    // Step 7: Validate that Student Email and Parent Email are lowercase and not empty
    for (let i = 2; i <= worksheet.rowCount; i++) {
      const row = worksheet.getRow(i);
      if (!row.hasValues) continue;
      const parentEmail = getEmailValue(row.getCell(parentEmailIndex + 1));
      if (parentEmail !== parentEmail.toLowerCase()) {
        throw new BadRequestException(
          `Invalid Parent / Guardian Email "${parentEmail}" for student "${row.getCell(headers.indexOf('Student Name') + 1).value}". Emails must be in lowercase only.`,
        );
      }
    }

  }
```
</details>

## Email Notifications for PG and Cash Payments

Once payments are initiated, the system sends out targeted email notifications based on the payment mode specified in the uploaded Excel file.

-   **PG (Payment Gateway) Payments**: For fees marked as `PG`, the system creates a `Pending` payment record. It then automatically sends a "Fee Due" email to the parent. This email includes a unique payment link, allowing the parent to complete the transaction online through the student portal.

-   **Cash Payments**: For fees marked as `CASH`, the system immediately creates a `Fully Paid` payment record. A "Payment Success" email is sent to the parent, confirming that the payment has been received and recorded. No further action is needed from the parent for this fee.

### Handling Mixed Payment Modes

The system is designed to handle cases where a student has both `PG` and `CASH` payments within the same bulk upload. In such scenarios, it ensures clarity by sending separate emails for each category:
One email for all outstanding payments with a link to pay.
  A separate confirmation email for all payments that have been successfully recorded as paid.

This ensures that parents have a clear understanding of what has been paid and what is still due.

The code that handles this logic has been enhanced to correctly process these scenarios.

## Cancel Payment Workflow

Institute administrators have the flexibility to cancel pending payments for one or more students. This can be done individually or in bulk.

### How It Works

  **Navigate to Payments**: The admin goes to **Fees Portal → Payment Collection** and selects a specific payment collection to view its items.

  **Select Payments to Cancel**: The admin can select payments using two methods:
    *   **Checkbox Selection**: Select individual rows by clicking the checkbox next to each payment record. A "select all" option is also available.
    *   **Nested Filtering**: Use the advanced filter options to narrow down the list of payments (e.g., by class, fee type, or due date) and then select all filtered results.

  **Cancel Action**: Once the desired records are selected, a **"Cancel Payment"** button becomes visible in the header.

  **Confirmation**: Clicking the button will prompt the admin for confirmation to prevent accidental cancellations.

### System Actions on Cancellation

Upon confirmation, the system performs the following actions:

-   **Status Update**: The `status` of the selected `PaymentCollectionItem` records is updated to `Cancelled`.
-   **Email Notification**: For each cancelled payment, the system sends a **"Payment Cancelled"** email to the parent's registered email address. This email clearly states which fee has been cancelled.

:::tip UI Preview
You can add a screenshot here showing the payment collection list view with checkboxes, the filter, and the "Cancel Payment" button in the header.
:::

### Code Snippet: Cancel Payment Logic

Here is a conceptual code snippet for the `cancelPayments` service method.

```typescript
@Injectable()
export class PaymentCollectionItemService {
  // ... other dependencies

  async cancelPayments(paymentItemIds: number[], instituteId: number): Promise<void> {
    //  Find the payment items to ensure they belong to the institute and are cancellable
    const itemsToCancel = await this.paymentCollectionItemRepo.find({
      where: {
        id: In(paymentItemIds),
        institute: { id: instituteId },
        status: 'Pending', // Only pending payments can be cancelled
      },
      relations: ['student', 'feeType', 'institute'],
    });

    if (itemsToCancel.length === 0) {
      throw new BadRequestException('No valid payments found for cancellation.');
    }

    //  Update the status of each item to 'Cancelled'
    const cancelledItemIds = itemsToCancel.map(item => item.id);
    await this.paymentCollectionItemRepo.update(cancelledItemIds, { status: 'Cancelled' });

    // 3. Trigger email notifications for each cancelled payment
    for (const item of itemsToCancel) {
      await this.sendCancellationEmail(item);
    }
  }

  private async sendCancellationEmail(item: PaymentCollectionItem) {
    const { student, feeType, institute } = item;
    
    // Use a mail service to send a templated email
    await this.mailService.sendPaymentCancelledMail({
      to: student.parentEmailAddress,
      studentName: student.studentName,
      feeTypeName: feeType.feeType,
      amount: item.amountToBePaid,
      instituteName: institute.name,
    });
  }
}
```

## Media Transaction Subscriber

This subscriber listens for new media uploads (the Excel file) and processes them.

#### Subscriber Entry Point (`paymentCollectionTransaction`)
This is the main method that gets triggered after the Excel file is uploaded. It reads the file and iterates through each row.
```Typescript
@EventSubscriber()
@Injectable()
export class MediaTransactionSubscriber implements EntitySubscriberInterface<Media> {

  private duplicateError: boolean = false;

  constructor(
    @InjectDataSource()
    private readonly dataSource: DataSource,
    @InjectRepository(Student)
    private readonly paymentService: PaymentService
  ) {
    this.dataSource.subscribers.push(this);
  }

  listenTo() {
    return Media;
  }

  async afterInsert(event: InsertEvent<Media>): Promise<void> {
    if (!event?.entity) {
      return;
    }
    const media = event.entity;
    const transactionManager = event.queryRunner?.manager;

    if (media.modelMetadata.singularName === 'paymentCollection' && media.fieldMetadata.name === 'paymentFile') {
      const isCompletedSuccessFully = await this.paymentCollectionTransaction(
        event,
        transactionManager
      );
    }
  }
}
```
### #Payment Collection Transaction Process

```Typescript
  private async paymentCollectionTransaction(event: InsertEvent<Media>, transactionManager: EntityManager) {
    const media = event.entity;
    const paymentCollectionRepo = transactionManager.getRepository(PaymentCollection);
    const paymentCollection = await paymentCollectionRepo.findOne({
      where: { id: media.entityId },
      relations: ['institute', 'institute.feeTypes'],
    });

    // Validation to check if the institute has feeTypes configured. 
    const feeTypes = paymentCollection.institute?.feeTypes;
    if (!feeTypes || feeTypes.length === 0) {
      throw new Error(`No fee types configured for institute: ${paymentCollection.institute || 'unable-to-resolve-institute'}`)
    }

    const folderPath = path.resolve(process.cwd(), 'media-files-storage/');
    const filePath = path.join(folderPath, media.relativeUri);
    const workbook = new ExcelJS.Workbook();
    await workbook.xlsx.readFile(filePath);
    const sheet = workbook.worksheets[0];
    if (!sheet) {
      console.error('Excel sheet not found!');
      return;
    }
    const headers: Record<string, number> = {};
    const headerRow = sheet.getRow(1);
    headerRow.eachCell((cell, colNumber) => {
      headers[cell.value as string] = colNumber;
    });

    for (let i = 2; i <= sheet.rowCount; i++) {
      const row = sheet.getRow(i);
      if (!row.hasValues) {
        continue;
      }
      const result = await this.processRow(row, paymentCollection, transactionManager, headers, event);
    }
  }
```

#### Row Processing Logic (`processRow`)
This function processes each row from the Excel file, creates student and payment records, and triggers email notifications.

<details>
<summary>Data Extraction and Student Creation</summary>

```typescript
  private async processRow(row: ExcelJS.Row, paymentCollection: PaymentCollection, transactionManager: any, headers: Record<string, number>, event: InsertEvent<Media>) {

    const studentRepo = transactionManager.getRepository(Student);
    const feeTypeRepo = transactionManager.getRepository(FeeType);
    const paymentCollectionItemRepo = transactionManager.getRepository(
      PaymentCollectionItem,
    );

    const parseDateToObject = (dateString: string): Date | null => {
      if (!dateString) return null; // Handle empty values
      const [day, month, year] = dateString.split('-').map(Number);
      return new Date(year, month - 1, day);
    };

    // adding new date test
    const formatDateToDDMMYYYY = (date: Date): string => {
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      return `${year}-${month}-${day}`;
    };

    const getCellValue = (headerName: string) => {
      if (headers[headerName] === undefined) return null;
      const cell = row.getCell(headers[headerName]);

      if (!cell || cell.value === null) return null;

      // Handle native Excel Date type
      if (cell.type === ExcelJS.ValueType.Date && cell.value instanceof Date) {
        return formatDateToDDMMYYYY(cell.value); // Convert to dd-mm-yyyy string
      }

      // Fallback to text
      return cell.text?.trim?.() ?? null;
    };

    // end
    const studentName = getCellValue('Student Name');
    const studentId = getCellValue('Student Id');
    const studentMobileNo = getCellValue('Student Mobile');
    const parentName = getCellValue('Parent / Guardian Name');
    const parentEmail = getCellValue('Parent / Guardian Email');
    const parentMobile = getCellValue('Parent / Guardian Mobile');
    const mode = getCellValue('Payment Mode').toUpperCase() || 'PG';

    let student = await studentRepo.findOne({
      where: { studentId, institute: { id: paymentCollection?.institute?.id }},
      relations: ['institute'],
    });
    if (!student) {
      student = studentRepo.create({
        studentName: studentName,
        parentName: parentName,
        parentMobileNumber: parentMobile,
        parentEmailAddress: parentEmail,
        studentId: studentId,
        institute: paymentCollection?.institute,
        studentMobileNumber: studentMobileNo,
      });
    }
    student.studentName = studentName;
    student.parentName = parentName;
    student.parentEmailAddress = parentEmail;
    student.parentMobileNumber = parentMobile;
    student.studentMobileNumber = studentMobileNo;
    student.instituteId = paymentCollection?.institute;

    const studentResult = await studentRepo.save(student);
```
</details>

<details>
<summary>Payment Item Creation</summary>

```typescript
    for (const feeType of paymentCollection.institute.feeTypes) {
      const amount = parseFloat(getCellValue(`${feeType.feeType}`) || '0');
      const dueDateStr = getCellValue(`${feeType.feeType} Due Date`);
      const dueDate = dueDateStr ? new Date(dueDateStr) : new Date(paymentCollection?.dueDate);
      const partPaymentAllowed = feeType?.partPaymentAllowed;

      if (amount > 0) {
        let status = 'Pending';
        let amountPaid = 0;
        let amountPending = amount;

        // If mode is CASH, mark as fully paid
        if (mode === 'CASH') {
          status = 'Fully Paid';
          amountPaid = amount;
          amountPending = 0;
        }

        const item = paymentCollectionItemRepo.create({
          student,
          paymentCollection,
          institute: paymentCollection.institute,
          feeType,
          dueDate: dueDate || new Date(),
          amountToBePaid: amount,
          partPaymentAllowed,
          status,
          amountPaid,
          amountPending,
          isOverdue: false,
          overdueByDays: 0,
          totalAmountToBePaid: amount,
          lateAmountToBePaid: 0,
          mode: mode,
        });

        await paymentCollectionItemRepo.save(item);
      }

    }
```
</details>

<details>
<summary>Email Notification Logic</summary>

```typescript
  // After saving items for this student...
  // Fetch all newly created items for this student in this payment collection
  const allItems = await paymentCollectionItemRepo.find({
      where: { 
        student: { studentLoginId: student.studentLoginId },
        paymentCollection: { id: paymentCollection.id }, 
      },
      relations: ['feeType', 'paymentCollection', 'student', 'institute'],
    });

    const fullyPaidItems = allItems.filter(i => i.status === 'Fully Paid');
    const pendingItems = allItems.filter(i => i.status === 'Pending');

    // CASE 1: Student has fully paid items (CASH mode) -> send a Success mail.
    if (fullyPaidItems.length > 0) {
      const feeTypes = [...new Set(fullyPaidItems.map(i => i.feeType?.feeType))].join(', ');
      const paymentCollections = [...new Set(fullyPaidItems.map(i => i.paymentCollection?.name))].join(', ');

      const createdAt = new Date().toLocaleDateString('en-US', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
      }).toUpperCase();

      await this.paymentService.sendPaymentSuccessMail(
        paymentCollection.institute.id,
        {
          student,
          amount: fullyPaidItems.reduce((sum, i) => sum + Number(i.amountPaid || 0), 0),
          feeTypes,
          paymentCollections,
          createdAt,
          institute: student.institute,
        },
        null,
        'success',
      );
    }

    // CASE 2: Student has pending items (PG mode) -> send a Due mail.
    if (pendingItems.length > 0) {
      const totalAmountDue = pendingItems.reduce((sum, i) => {
        const totalAmountToBePaid = Number(i.totalAmountToBePaid) || 0;
        const amountPaid = Number(i.amountPaid) || 0;
        return sum + (totalAmountToBePaid - amountPaid);
      }, 0);
      const feeTypes = [...new Set(pendingItems.map(i => i.feeType?.feeType))].join(', ');
      const paymentCollections = [...new Set(pendingItems.map(i => i.paymentCollection?.name))].join(', ');

      const createdAt = new Date().toLocaleDateString('en-US', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
      }).toUpperCase();

      const dueFees = {
        totalAmountDue,
        feeTypes,
        status: 'Pending',
        redirectUrl: `https://${pendingItems?.[0].institute.hostedPagePrefix}-${process.env.TEMPLE_BASE_DOMAIN}/?id=${student.studentLoginId}`,
        createdAt,
        paymentCollections,
        parentEmailAddress: student.parentEmailAddress,
        student,
      };

      await this.paymentService.sendDueFeesMail(dueFees, paymentCollection.institute.id);
    }
  }
```
</details>

## Automated Due-Date Reminders

The system also sends automated reminders for overdue or upcoming payment deadlines.

| Type                          | Trigger                                                        |
| ----------------------------- | -------------------------------------------------------------- |
| **Upcoming Due Reminder**     | Before the due date (optional, configurable)                   |
| **Overdue Reminder**          | When due date passes and payment remains pending               |
| **Multi-Frequency Reminders** | Daily / Weekly / Monthly / Yearly (configurable per institute) |

### Reminder Behavior

Only Pending payments are processed.
Payments marked as Paid (including Cash mode) are ignored by all schedulers and subscribers.

Each reminder email includes:

- Outstanding amount
- Updated due date or overdue warning
- Payment link

### 📩 Email Template Preview

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/email-remainder.png)

### Initial Notification Logic
```Typescript
    async sendDueFeesMail(dueFees: any, instituteId: number) {
    //  Fetch Institue by Name then take Id and call another
    const institute = await this.instituteService.findOne(instituteId || 0, {
      populateMedia: ['logo']
    });
    // 5. Send mail
      const mailService = this.mailServiceFactory.getMailService();
      await mailService.sendEmailUsingTemplate(
        dueFees.parentEmailAddress,
        'new-payment-or-payment-reminder',
        { 
          dueDetails: dueFees,
          instituteLogo:institute._media.logo[0]._full_url,
          student: dueFees.student,
        },
        true,
        [],
        [],
        null,
        null,
      );
  }
```

:::tip Email Processing (Background Job)
All payment notifications and reminders use SolidX’s  
**`sendEmailUsingTemplate()`** method, which automatically pushes each email into the **internal queue** (DB queue or RabbitMQ, depending on configuration).

This ensures:
- Emails are processed **asynchronously**  
- No blocking during Initiate Payment  
- Automatic retry handling  
- High-volume institutes can send thousands of emails without performance issues  
- You can subscribe to the queue and process messages in the background

The upcoming code example will show how the queue subscriber picks up email jobs and executes them efficiently.
:::


## Email Notification Queue – Architecture & Flow

### (Database Queue / RabbitMQ Compatible – Using SolidX Publishers & Subscribers)

This module handles asynchronous email notifications for payment initiation, reminders, and due-fee alerts.
It uses SolidX’s DatabasePublisher / DatabaseSubscriber abstraction to push email jobs into a queue and process them in the background

###  Queue Publisher (Database / RabbitMQ)

Responsible for publishing email jobs to the queue.

`mswipe-notify-api-email-publisher-database.service.ts`

```Typescript
  // MswipeNotifyApiEmailQueuePublisherDatabase
import { Injectable } from '@nestjs/common';

import mailQueueOptions from './mswipe-notify-api-email-queue-options-database';
import {
    MqMessageService,
    MqMessageQueueService,
    QueuesModuleOptions,
    DatabasePublisher
} from '@solidstarters/solid-core';

@Injectable()
export class MswipeNotifyApiEmailQueuePublisherDatabase extends DatabasePublisher<any> {
    constructor(
        protected readonly mqMessageService: MqMessageService,
        protected readonly mqMessageQueueService: MqMessageQueueService,
    ) {
        super(mqMessageService, mqMessageQueueService);
    }

    options(): QueuesModuleOptions {
        return {
            ...mailQueueOptions,
        };
    }
}
```

###  Queue Options File

`mswipe-notify-api-email-queue-options-database.ts`

```Typescript
    import { BrokerType } from "@solidstarters/solid-core";

const API_MAIL_QUEUE_NAME = 'mswipe_notify_api_email_queue_database';

export default {
    name: 'mswipeNotifyApiEmailQueueDatabase',
    type: BrokerType.Database,       // Can be swapped with RabbitMQ without changing publisher/subscriber code
    queueName: API_MAIL_QUEUE_NAME,
};
```
### 3. Queue Subscriber (Background Worker)

`mswipe-notify-api-email-subscriber-database.service.ts`

```Typescript
// mswipe-notify-api-email-subscriber-database.service
import { Injectable } from '@nestjs/common';
import {
    MqMessageService,
    MqMessageQueueService,
    QueuesModuleOptions,
    QueueMessage,
    DatabaseSubscriber,
    PollerService
} from '@solidstarters/solid-core';

import { MswipeNotifyApiEmailService } from 'src/fees-portal/services/mswipe-notify-api-email.service';
import mailQueueOptions from './mswipe-notify-api-email-queue-options-database';

@Injectable()
export class MswipeNotifyApiEmailQueueSubscriberDatabase extends DatabaseSubscriber<any> {
    constructor(
        private readonly emailService: MswipeNotifyApiEmailService,
        readonly mqMessageService: MqMessageService,
        readonly mqMessageQueueService: MqMessageQueueService,
        readonly pollerService: PollerService,
    ) {
        super(mqMessageService, mqMessageQueueService, pollerService);
    }

    options(): QueuesModuleOptions {
        return {
            ...mailQueueOptions,
        };
    }

    subscribe(message: QueueMessage<any>) {
        this.emailService.sendEmailSynchronously(message);
    }
}

```

## Cancel Payment Workflow

The Cancel Payment feature allows Institute Admins to cancel one or multiple pending payment records.
Admins can cancel:

- Individual Payment Collection Items
- Entire Payment Collections (parent records)
- Bulk selections using checkboxes

### Using nested UI filters (without selecting IDs manually)

Once cancelled:

- Payment status changes to Cancelled
- Parent receives Cancellation Notification Email
- Email is processed asynchronously using queue-based background workers

```Typescript
@ApiBearerAuth("jwt")
@Post("/cancel-payment-collection")
async cancelMany(@Body() body: { 
  collectionIds: any[], 
  ids: any[], 
  filters?: any, 
  modelName: string 
}) {
  return this.service.cancelPaymentCollectionItems(
    body.collectionIds,
    body.ids,
    body.filters || {},
    body.modelName
  );
}
```

### How Cancellation Works

Payment Collection → Payment Collection Items → Cancel Button

Supported actions:
- Cancel by selecting checkboxes

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/cancel1.png)

- Cancel all filtered records

![Initial Payment Notification Email](/img/tutorial/school-fees-portal/6-usecase/cancel2.png)

- Cancel entire fee collections
- Cancel pending dues for specific fee types

:::tip
Only payments with status = Pending are eligible.
:::

### Backend Logic Summary

```Typescript
const pendingItemsData = await this.find(query);
const pendingItems = pendingItemsData.records;
```
### Bulk Cancel Operation

```Typescript
await this.repo.update(
  { id: In(pendingIds) },
  { status: "Cancelled" }
);
```
### Group Cancelled Items by Parent Email

Ensures one email per parent, even if multiple items were cancelled.

```Typescript
itemsByParent.set(parentEmail, { student, institute, items: [] });
```

### Cancel Email Notifications

```Typescript
{
  "paymentDetails": {
    "txnId": "MSW123456",
    "totalAmountDue": "1200.00",
    "feeTypes": ["Term Fee", "Library Fee"],
    "status": "Cancelled"
  },
  "student": {
    "studentName": "Rahul Sharma"
  }
}
```