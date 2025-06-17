---
sidebar_position: 5
---

# 4. Customisations

Welcome to SolidX admin documentation! SolidX is an enterprise-focused, low-code development platform engineered for today's web applications. 

In our tutorial, the **Institute** model requires uploading various types of media such as **logo images**, **brochures**, and **intro videos**. SolidX makes this process simple by providing built-in support for two media storage options:

- **AWS S3**: A cloud storage option using your own S3 bucket.
- **Default File System**: A local storage method that uses `multer` to store files in the `./media-uploads` directory.

SolidX abstracts away the complexity, allowing you to configure either of these with just a few steps. We'll first walk through how to enable AWS S3 as your media provider, and then how to set up the default local file system.

## Enable S3 as a media provider

To enable media uploads to AWS S3, follow these steps as a **Solid Admin**:

### Step 1: Select Media Storage Provider
1. While creating or editing a model field of type **Media**, scroll to the **Advanced Configuration** section.
2. From the **Media Storage Provider** dropdown, select **Default aws S3**.

![Default Login Page](/img/tutorial/school-fees-portal/4-customization/default-file-sytem.png)

### Step 2: Access Media Storage Providers
1. Go to the Solid Admin panel.
2. Navigate to **Media** → **Media Storage Providers**.
3. You will see two storage options:
   - **AWS S3 List**
   - **Default File System**

### Step 3: Edit the AWS S3 Configuration
1. Click **Edit** on the **AWS S3 List** item.
2. Fill in the following required fields:
   - **Region**: Your AWS region (e.g., `us-east-1`)
   - **Bucket Name**: The name of your S3 bucket
3. If your AWS S3 bucket is private, also set the Signed URL Expiry value (in minutes).
    This defines how long the signed URL will remain valid when retrieving media files from the private bucket. 

4. Click **Save** to store the configuration.

### Step 4: Update Environment Variables
Ensure your `.env` file includes the following keys:

```env
S3_AWS_ACCESS_KEY=your-access-key
S3_AWS_SECRET_KEY=your-secret-key
S3_AWS_REGION_NAME=your-region-name
```

## Enable Filesystem as a media provider 


To store media files on the local **File System**, follow the steps below while configuring your model:

### Step 1: Select Media Storage Provider
1. While creating or editing a model field of type **Media**, scroll to the **Advanced Configuration** section.
2. From the **Media Storage Provider** dropdown, select **Default File System**.

![Default Login Page](/img/tutorial/school-fees-portal/4-customization/default-file-sytem.png)

This setting ensures that uploaded media for this field will be stored on the server's local file system instead of an external service like AWS S3.

All uploaded files will be physically stored inside the
media-uploads/ folder.

### Step 2: Set Base URL in Environment File
In your `.env` file, make sure to include the base URL for accessing locally stored media:

```env
BASE_URL=http://your-domain.com/media
```

## Extending the SolidX user model  

You can extend the built-in **SolidX User** model to attach additional fields or relationships required by your application. Follow the steps below to do this from the **App Builder**:

### Step 1: Navigate to Model Creation
1. Go to the **SolidX Module**.
2. Click on **App Builder** → **Models**.
3. Create a new model or open an existing one that you want to extend.

### Step 2: Enable as Child of SolidX User
1. In the **Model Creation** screen, fill in all the required fields like **Name**, **Display Name**, etc.
2. Scroll down to the **Configuration** section.
3. Enable the **Is Child** checkbox.
4. A dropdown will appear — select **SolidX User** from the list.

![Default Login Page](/img/tutorial/school-fees-portal/4-customization/extend-solidx-user-model.png)

> ✅ Once selected, your model will now **extend the SolidX User model**, allowing it to inherit its core identity fields while adding your own custom fields.


## Custom home page for the module
When you create a new module in SolidX, a custom home page is automatically generated for that module.

![Default Login Page](/img/tutorial/school-fees-portal/4-customization/home.png)

This custom home page acts as a dashboard for the module and provides the following features:

✅ A visual overview of the module data (charts, stats, or cards).

➕ Quick access buttons to create new entries for the module.

📄 Shortcuts to manage Models, Fields, and other module-related configurations.
You can access this page from the left-hand sidebar by clicking the module name under that you can se Home. It is designed to help module admins manage and understand their module data at a glance, without needing to manually configure a dashboard.

## Computed fields 
## Subscribers 
### Consume the payment file