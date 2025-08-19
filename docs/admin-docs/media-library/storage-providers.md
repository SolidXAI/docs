---
sidebar_position: 2
---

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




### Upcoming Providers ###
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


<div className="border-box">
    <h4 className="card-title">
    ### Common Features ###
    </h4>
    - File upload/download
    - Directory operations
    - Access control
    - Metadata management
</div>

### Provider-Specific Features

<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">
    ### 1 Local Filesystem ###
    </h4>
    <ul className="card-desc">
      <li>Direct file access</li>
      <li>System-level permissions</li>
      <li>Local caching</li>
      <li>Path customization</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">
    ### 2 Amazon S3 ###
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

## Best Practices

<!-- 1. **Provider Selection**
   - Consider scalability needs
   - Evaluate cost implications
   - Assess performance requirements
   - Plan for redundancy

2. **Security**
   - Use secure credentials
   - Implement proper ACLs
   - Enable encryption
   - Regular security audits

3. **Performance**
   - Configure caching
   - Optimize file sizes
   - Use CDN when possible
   - Monitor usage patterns

4. **Maintenance**
   - Regular backups
   - Monitor storage usage
   - Clean up unused files
   - Update configurations -->


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Provider Selection</h4>
    <ul className="card-desc">
      <li>Consider scalability needs</li>
      <li>Evaluate cost implications</li>
      <li>Assess performance requirements</li>
      <li>Plan for redundancy</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Security</h4>
    <ul className="card-desc">
      <li>Use secure credentials</li>
      <li>Implement proper ACLs</li>
      <li>Enable encryption</li>
      <li>Regular security audits</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3 Performance</h4>
    <ul className="card-desc">
      <li>Configure caching</li>
      <li>Optimize file sizes</li>
      <li>Use CDN when possible</li>
      <li>Monitor usage patterns</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">4 Maintenance</h4>
    <ul className="card-desc">
      <li>Regular backups</li>
      <li>Monitor storage usage</li>
      <li>Clean up unused files</li>
      <li>Update configurations</li>
    </ul>
  </div>

</div>



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
<!-- 
3. **Set Up Permissions**
- Configure access credentials
- Set up network access
- Define security policies

4. **Test Configuration**
- Upload test file
- Verify access
- Check permissions
- Validate features -->


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">3 Set Up Permissions</h4>
    <ul className="card-desc">
      <li>Configure access credentials</li>
      <li>Set up network access</li>
      <li>Define security policies</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">4 Test Configuration</h4>
    <ul className="card-desc">
      <li>Upload test file</li>
      <li>Verify access</li>
      <li>Check permissions</li>
      <li>Validate features</li>
    </ul>
  </div>

</div>


### Migration Between Providers

<!-- 1. **Preparation**
   - Inventory existing files
   - Plan migration schedule
   - Test migration process
   - Prepare rollback plan

2. **Execution**
   - Copy files to new provider
   - Verify file integrity
   - Update references
   - Switch provider settings

3. **Verification**
   - Test file access
   - Verify permissions
   - Check performance
   - Monitor errors -->


<div className="feature-grid">

  <div className="feature-card">
    <h4 className="card-title">1 Preparation</h4>
    <ul className="card-desc">
      <li>Inventory existing files</li>
      <li>Plan migration schedule</li>
      <li>Test migration process</li>
      <li>Prepare rollback plan</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">2 Execution</h4>
    <ul className="card-desc">
      <li>Copy files to new provider</li>
      <li>Verify file integrity</li>
      <li>Update references</li>
      <li>Switch provider settings</li>
    </ul>
  </div>

  <div className="feature-card">
    <h4 className="card-title">3 Verification</h4>
    <ul className="card-desc">
      <li>Test file access</li>
      <li>Verify permissions</li>
      <li>Check performance</li>
      <li>Monitor errors</li>
    </ul>
  </div>

</div>
