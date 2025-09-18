---
sidebar_position: 5
---

# Computed Fields

In SolidX, Computed Fields are used to automatically calculate field values based on other data. These fields aren’t manually entered by users but are filled during lifecycle events like afterInsert or afterUpdate. They help keep data consistent and reduce manual effort.

### Creating a Computed Field
You can define a computed field through the UI by following these steps:

- Go to the Model where you want to add the computed field.

- Add or edit a field, and set its Field Type to Computed.

- Navigate to the Advanced Config tab (as shown in the screenshot).

Configure the computed logic:

- Computed Field Value Type: (optional) The expected type (e.g., number, string).

- Computed Field Provider: Select a provider (e.g., PaymentCollectionItemAmountProvider) that contains the logic for calculation.

- Trigger Config: Define when the computation should be triggered by choosing:

- Module and Model the field belongs to.

- Operations like afterInsert, afterUpdate, etc.

![Default Login Page](/img/tutorial/school-fees-portal/4-customization/computed-field.png)

Code Sample Here's a trimmed view of how this computed fields implementation looks:

```tsx
import { Injectable } from '@nestjs/common';
import {
  ComputedFieldProvider,
  CommonEntity,
  IEntityPreComputeFieldProvider,
  IEntityPostComputeFieldProvider,
  ComputedFieldMetadata,
} from '@solidstarters/solid-core';
import { kebabCase } from 'lodash';
import { PaymentCollectionItemDetail } from '../entities/payment-collection-item-detail.entity';
import { EntityManager } from 'typeorm';
import { InjectEntityManager } from '@nestjs/typeorm';
import { PaymentCollectionItem } from '../entities/payment-collection-item.entity';
import { error } from 'console';

@ComputedFieldProvider()
@Injectable()
export class PaymentCollectionItemAmountProvider
  implements IEntityPostComputeFieldProvider<PaymentCollectionItemDetail, any>
{
  constructor(
    @InjectEntityManager()
    private readonly entityManager: EntityManager,
  ) {}
  async postComputeAndSaveValue(
    triggerEntity: PaymentCollectionItemDetail,
    computedFieldMetadata: ComputedFieldMetadata<any>,
  ): Promise<void> {
    if (!triggerEntity?.paymentCollectionItem?.id) {
      throw new error('Payment Collection Item Id Missing');
    }
    const paymentCollectionItemDetailId = triggerEntity?.id;
    const { amountPaid, totalamounttobepaid, amountPending, status } =
      await this.getPaymentCollectionItemAmounts(
        triggerEntity?.paymentCollectionItem?.id,
      );
    const result = await this.entityManager.update(
      PaymentCollectionItem,
      { id: triggerEntity?.paymentCollectionItem?.id },
      {
        amountPaid: amountPaid,
        amountPending: amountPending,
        totalAmountToBePaid: totalamounttobepaid,
        status: status,
      },
    );
  }

  name(): string {
    return 'PaymentCollectionItemAmountProvider';
  }

  help(): string {
    return 'Payment Collection ItemA mountProvider field provider used to create fields whose value is a concatenation of other fields in the same model.';
  }

  private async getPaymentCollectionItemAmounts(itemId: number): Promise<{
    amountPaid: number;
    totalamounttobepaid: number;
    amountPending: number;
    status: string;
  }> {
    const details = await this.entityManager.find(PaymentCollectionItemDetail, {
      where: { paymentCollectionItem: { id: itemId } },
      relations: ['paymentCollectionItem'],
    });

    const amountPaid = details.reduce(
      (sum, detail) => sum + Number(detail.amountPaid || 0),
      0,
    );
    const paymentCollectionItem = details[0]?.paymentCollectionItem;
    const totalamounttobepaid =
      Number(paymentCollectionItem?.amountToBePaid || 0) +
      Number(paymentCollectionItem?.lateAmountToBePaid || 0);

    const amountPending = totalamounttobepaid - amountPaid;

    const status = amountPending > 0 ? 'Partially Paid' : 'Fully Paid';

    return { amountPaid, totalamounttobepaid, amountPending, status };
  }
}

```
