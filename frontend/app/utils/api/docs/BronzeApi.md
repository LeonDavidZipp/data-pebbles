# BronzeApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**bronzeCreateResource**](BronzeApi.md#bronzecreateresource) | **POST** /bronze/ | Create Resource |
| [**bronzeDeleteResource**](BronzeApi.md#bronzedeleteresource) | **DELETE** /bronze/{resource_id} | Delete Resource |
| [**bronzeDownloadVersion**](BronzeApi.md#bronzedownloadversion) | **GET** /bronze/{resource_id}/versions/{version} | Download Version |
| [**bronzeGetResource**](BronzeApi.md#bronzegetresource) | **GET** /bronze/{resource_id} | Get Resource |
| [**bronzeGetSchema**](BronzeApi.md#bronzegetschema) | **GET** /bronze/{resource_id}/versions/{version}/schema | Get Schema |
| [**bronzeListResources**](BronzeApi.md#bronzelistresources) | **GET** /bronze/ | List Resources |
| [**bronzeListVersions**](BronzeApi.md#bronzelistversions) | **GET** /bronze/{resource_id}/versions | List Versions |
| [**bronzeUpdateResource**](BronzeApi.md#bronzeupdateresource) | **PATCH** /bronze/{resource_id} | Update Resource |
| [**bronzeUploadVersion**](BronzeApi.md#bronzeuploadversion) | **POST** /bronze/{resource_id}/versions | Upload Version Single |



## bronzeCreateResource

> CreateResourceResponse bronzeCreateResource(createResourceRequest)

Create Resource

Creates a new resource in the layer.  Args:         body: A CreateResourceRequest object containing the name, project ID, and                 optional description for the new resource.         loader: The loader instance to use for creating the resource.  Returns:         A CreateResourceResponse containing a success message and the ID of the         newly created resource.

### Example

```ts
import {
  Configuration,
  BronzeApi,
} from '';
import type { BronzeCreateResourceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new BronzeApi();

  const body = {
    // CreateResourceRequest
    createResourceRequest: ...,
  } satisfies BronzeCreateResourceRequest;

  try {
    const data = await api.bronzeCreateResource(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **createResourceRequest** | [CreateResourceRequest](CreateResourceRequest.md) |  | |

### Return type

[**CreateResourceResponse**](CreateResourceResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## bronzeDeleteResource

> MessageResponse bronzeDeleteResource(resourceId)

Delete Resource

Deletes the specified resource.  Args:         resource_id: The ID of the resource to delete.         loader: The loader instance to use for deleting the resource.  Returns:         A MessageResponse indicating the result of the delete operation.

### Example

```ts
import {
  Configuration,
  BronzeApi,
} from '';
import type { BronzeDeleteResourceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new BronzeApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies BronzeDeleteResourceRequest;

  try {
    const data = await api.bronzeDeleteResource(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **resourceId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**MessageResponse**](MessageResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## bronzeDownloadVersion

> any bronzeDownloadVersion(resourceId, version)

Download Version

Downloads the specified version of the resource as a Parquet file.  Args:         resource_id: The ID of the resource.         version: The version number of the resource.         loader: The loader instance to use for fetching the data.  Returns:         A StreamingResponse containing the Parquet file.

### Example

```ts
import {
  Configuration,
  BronzeApi,
} from '';
import type { BronzeDownloadVersionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new BronzeApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies BronzeDownloadVersionRequest;

  try {
    const data = await api.bronzeDownloadVersion(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **resourceId** | `number` |  | [Defaults to `undefined`] |
| **version** | `number` |  | [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## bronzeGetResource

> MetadataResponse bronzeGetResource(resourceId)

Get Resource

Retrieves the metadata of the specified resource.  Args:         resource_id: The ID of the resource to retrieve.         loader: The loader instance to use for fetching the metadata.  Returns:         A MetadataResponse object containing the metadata of the resource.

### Example

```ts
import {
  Configuration,
  BronzeApi,
} from '';
import type { BronzeGetResourceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new BronzeApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies BronzeGetResourceRequest;

  try {
    const data = await api.bronzeGetResource(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **resourceId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**MetadataResponse**](MetadataResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## bronzeGetSchema

> SchemaResponse bronzeGetSchema(resourceId, version)

Get Schema

Returns the schema of the specified version of the resource.  Args:         resource_id: The ID of the resource.         version: The version number of the resource.         loader: The loader instance to use for fetching the data.  Returns:         A SchemaResponse containing the data schema and a sample of the data.

### Example

```ts
import {
  Configuration,
  BronzeApi,
} from '';
import type { BronzeGetSchemaRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new BronzeApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies BronzeGetSchemaRequest;

  try {
    const data = await api.bronzeGetSchema(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **resourceId** | `number` |  | [Defaults to `undefined`] |
| **version** | `number` |  | [Defaults to `undefined`] |

### Return type

[**SchemaResponse**](SchemaResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## bronzeListResources

> Array&lt;MetadataResponse&gt; bronzeListResources()

List Resources

Lists all resources in the layer.  Args:         loader: The loader instance to use for fetching the metadata.  Returns:         A list of MetadataResponse objects containing the metadata of all resources.

### Example

```ts
import {
  Configuration,
  BronzeApi,
} from '';
import type { BronzeListResourcesRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new BronzeApi();

  try {
    const data = await api.bronzeListResources();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**Array&lt;MetadataResponse&gt;**](MetadataResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## bronzeListVersions

> Array&lt;LineageResponse&gt; bronzeListVersions(resourceId)

List Versions

Lists all versions of the specified resource along with their lineage information.  Args:         resource_id: The ID of the resource to list versions for.         loader: The loader instance to use for fetching the lineage information.  Returns:         A list of LineageResponse objects representing the versions of the resource.

### Example

```ts
import {
  Configuration,
  BronzeApi,
} from '';
import type { BronzeListVersionsRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new BronzeApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies BronzeListVersionsRequest;

  try {
    const data = await api.bronzeListVersions(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **resourceId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**Array&lt;LineageResponse&gt;**](LineageResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## bronzeUpdateResource

> MetadataResponse bronzeUpdateResource(resourceId, updateResourceRequest)

Update Resource

Updates the metadata of the specified resource.  Args:         resource_id: The ID of the resource to update.         body: An UpdateResourceRequest object containing the new name and                 description for the resource.         loader: The loader instance to use for updating the metadata.  Returns:         A MetadataResponse object containing the updated metadata of the resource.

### Example

```ts
import {
  Configuration,
  BronzeApi,
} from '';
import type { BronzeUpdateResourceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new BronzeApi();

  const body = {
    // number
    resourceId: 56,
    // UpdateResourceRequest
    updateResourceRequest: ...,
  } satisfies BronzeUpdateResourceRequest;

  try {
    const data = await api.bronzeUpdateResource(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **resourceId** | `number` |  | [Defaults to `undefined`] |
| **updateResourceRequest** | [UpdateResourceRequest](UpdateResourceRequest.md) |  | |

### Return type

[**MetadataResponse**](MetadataResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## bronzeUploadVersion

> MessageResponse bronzeUploadVersion(resourceId, fromResourceId, file)

Upload Version Single

Uploads a new version of the resource from a Parquet file.  Args:         resource_id: The ID of the resource to upload a new version for.         file: The uploaded Parquet file containing the new version of the data.         loader: The loader instance to use for uploading the data.         from_resource_id: The ID of the existing resource version that this new                 version is derived from.  Returns:         A MessageResponse indicating the result of the upload operation.

### Example

```ts
import {
  Configuration,
  BronzeApi,
} from '';
import type { BronzeUploadVersionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new BronzeApi();

  const body = {
    // number
    resourceId: 56,
    // number
    fromResourceId: 56,
    // string
    file: file_example,
  } satisfies BronzeUploadVersionRequest;

  try {
    const data = await api.bronzeUploadVersion(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **resourceId** | `number` |  | [Defaults to `undefined`] |
| **fromResourceId** | `number` |  | [Defaults to `undefined`] |
| **file** | `string` |  | [Defaults to `undefined`] |

### Return type

[**MessageResponse**](MessageResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `multipart/form-data`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

