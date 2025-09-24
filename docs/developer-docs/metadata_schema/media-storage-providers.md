---
title: Media Storage Providers Metadata
description: Metadata schema for defining media storage providers in SolidX applications.
sidebar_position: 11
---

## Overview
SOLID supports multiple storage providers for media files, offering flexibility in how and where your media assets are stored.
For a conceptual overview of media storage providers in SolidX, refer to the [Storage Providers](../../admin-docs/media-library/storage-providers.md).

## Example: Media Storage Providers Metadata
<details>
<summary> Media Storage Providers Schema </summary>
``` json
{
  ..., // Other metadata
  "mediaStorageProviders": [
    {
      "name": "default-filesystem", // This is seeded by default, no need to mention it in json. Provided here just for reference.
      "type": "filesystem"
    },
    {
      "name": "default-aws-s3", // This is seeded by default, no need to mention it in json. Provided here just for reference. 
      "type": "aws-s3"
    }
  ],
}
```
</details>
:::info
For the media storage provider `default-aws-s3`, you need to provide the following environment variables in your `.env` file or deployment environment:

```bash
S3_AWS_ACCESS_KEY=<YOUR_ACCESS_KEY>    # Only in env, not JSON (for security)
S3_AWS_SECRET_KEY=<YOUR_SECRET_KEY>    # Only in env, not JSON (for security)
S3_AWS_REGION_NAME=<YOUR_AWS_REGION>   # Can also be specified in JSON
S3_BUCKET_NAME=<YOUR_BUCKET_NAME>      # Can also be specified in JSON
```
:::

## Media Storage Providers Metadata Attributes

### `name` *(string, required, unique)*
Name of the media storage provider (column/property).

### `type` *(string, required)*
Type of the media storage provider. Supported types include:
- `filesystem`: Local filesystem storage.
- `aws-s3`: Amazon S3 storage.
- Other types like `azure-blob-storage` can be added in the future.

### `region` *(string, optional)*
Region for the storage provider (applicable for cloud providers like AWS S3).
**Applies to** `aws-s3`

### `bucketName` *(string, optional)*
Name of the bucket/container where media files will be stored (applicable for cloud providers like AWS S3).
**Applies to** `aws-s3`

### `isPublic` *(boolean, optional)*
Indicates whether the media files stored in this provider are publicly accessible.
**Applies to** `aws-s3`

### `signedUrlExpiry` *(number, optional)*
Expiry time (in minutes) for signed URLs generated for accessing private media files.
**Applies to** `aws-s3`