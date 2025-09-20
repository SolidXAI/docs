--- 
title: Storage Providers
description: Overview of supported media storage providers in SolidX applications.
sidebar_position: 2
---

import { FaPlay, FaCheckCircle, FaCogs,FaHdd, FaAws} from "react-icons/fa"
import { IoIosArrowForward } from "react-icons/io";
import { WarningBox } from '@site/src/common/WarningBox';

<WarningBox>
  Work in Progress - This document is currently being updated. Some sections may be incomplete or subject to change.
</WarningBox>


<br/>

# Storage Providers

SOLID supports multiple storage providers for media files, offering flexibility in how and where your media assets are stored.

## Supported Providers

### Local Filesystem

- **Description**: Store files directly on the server's filesystem
- **Use Case**: Development environments, small applications
- **Configuration**:

```json
{
  "provider": "local",
  "config": {
    "rootPath": "/path/to/uploads",
    "baseUrl": "http://your-domain.com/uploads"
  }
}
```

### Amazon S3

- **Description**: Store files in Amazon S3 buckets
- **Use Case**: Production environments, scalable applications
- **Configuration**:

```json
{
  "provider": "s3",
  "config": {
    "accessKeyId": "YOUR_ACCESS_KEY",
    "secretAccessKey": "YOUR_SECRET_KEY",
    "region": "us-west-2",
    "bucket": "your-bucket-name",
    "baseUrl": "https://your-bucket.s3.amazonaws.com"
  }
}
```

<!-- ### Upcoming Providers
- Azure Blob Storage
- Google Cloud Storage
- SFTP
- Custom providers -->

### Upcoming Providers

- Azure Blob Storage
- Google Cloud Storage
- SFTP
- Custom providers

## Provider Features

<!-- ### Common Features
All storage providers support:
- File upload/download
- Directory operations
- Access control
- Metadata management -->

  <h3 className="card-title">
    Common Features 
  </h3>
  - File upload/download
  - Directory operations
  - Access control
  - Metadata management

### Provider-Specific Features


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaHdd size={16} style={{ marginRight: "10px" }} />
      Local Filesystem
    </h4>
    <ul className="card-desc">
      <li>Direct file access</li>
      <li>System-level permissions</li>
      <li>Local caching</li>
      <li>Path customization</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaAws size={16} style={{ marginRight: "10px" }} />
      Amazon S3
    </h4>
    <ul className="card-desc">
      <li>Bucket policies</li>
      <li>CloudFront integration</li>
      <li>Lifecycle rules</li>
      <li>Versioning</li>
      <li>Cross-region replication</li>
    </ul>
  </div>

</div>


## Configuration

### Global Settings

```json
{
  "defaultProvider": "s3",
  "uploadLimits": {
    "maxFileSize": "100MB",
    "allowedTypes": ["image/*", "application/pdf"]
  },
  "imageProcessing": {
    "thumbnails": true,
    "maxWidth": 2000,
    "maxHeight": 2000
  }
}
```

### Provider Selection

Files can be routed to different providers based on:

- File type
- File size
- User role
- Custom rules



## Implementation Guide

### Adding a New Provider

1. **Install Dependencies**

```bash
npm install @solid/storage-provider-name
```

2. **Configure Provider**

```json
{
  "providers": {
    "custom-provider": {
      "implementation": "@solid/storage-provider-name",
      "config": {
        // Provider-specific configuration
      }
    }
  }
}
```


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      3 Set Up Permissions
    </h4>
    <ul className="card-desc">
      <li>Configure access credentials</li>
      <li>Set up network access</li>
      <li>Define security policies</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      4 Test Configuration
    </h4>
    <ul className="card-desc">
      <li>Upload test file</li>
      <li>Verify access</li>
      <li>Check permissions</li>
      <li>Validate features</li>
    </ul>
  </div>

</div>

### Migration Between Providers

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaCogs size={16} style={{ marginRight: "10px" }} />
      1 Preparation
    </h4>
    <ul className="card-desc">
      <li>Inventory existing files</li>
      <li>Plan migration schedule</li>
      <li>Test migration process</li>
      <li>Prepare rollback plan</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaPlay size={14} style={{ marginRight: "10px" }} />
      2 Execution
    </h4>
    <ul className="card-desc">
      <li>Copy files to new provider</li>
      <li>Verify file integrity</li>
      <li>Update references</li>
      <li>Switch provider settings</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title card-headear-wrapper">
      <FaCheckCircle size={16} style={{ marginRight: "10px" }} />
      3 Verification
    </h4>
    <ul className="card-desc">
      <li>Test file access</li>
      <li>Verify permissions</li>
      <li>Check performance</li>
      <li>Monitor errors</li>
    </ul>
  </div>

</div>



## Best Practices

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
     Provider Selection
  </summary>
  <ul className="card-desc">
    <li>Consider scalability needs</li>
    <li>Evaluate cost implications</li>
    <li>Assess performance requirements</li>
    <li>Plan for redundancy</li>
  </ul>
</details>

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
     Security
  </summary>
  <ul className="card-desc">
    <li>Use secure credentials</li>
    <li>Implement proper ACLs</li>
    <li>Enable encryption</li>
    <li>Regular security audits</li>
  </ul>
</details>

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
     Performance
  </summary>
  <ul className="card-desc">
    <li>Configure caching</li>
    <li>Optimize file sizes</li>
    <li>Use CDN when possible</li>
    <li>Monitor usage patterns</li>
  </ul>
</details>

<details>
  <summary className="card-title card-headear-wrapper">
    <IoIosArrowForward size={20} style={{ marginRight: "8px" }} className="rotatable" />
     Maintenance
  </summary>
  <ul className="card-desc">
    <li>Regular backups</li>
    <li>Monitor storage usage</li>
    <li>Clean up unused files</li>
    <li>Update configurations</li>
  </ul>
</details>
