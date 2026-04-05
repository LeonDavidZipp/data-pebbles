# SilverApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**silverCreateResource**](SilverApi.md#silvercreateresource) | **POST** /silver/ | Create Resource |
| [**silverDeleteResource**](SilverApi.md#silverdeleteresource) | **DELETE** /silver/{resource_id} | Delete Resource |
| [**silverDownloadVersion**](SilverApi.md#silverdownloadversion) | **GET** /silver/{resource_id}/versions/{version} | Download Version |
| [**silverGetResource**](SilverApi.md#silvergetresource) | **GET** /silver/{resource_id} | Get Resource |
| [**silverGetSchema**](SilverApi.md#silvergetschema) | **GET** /silver/{resource_id}/versions/{version}/schema | Get Schema |
| [**silverListResources**](SilverApi.md#silverlistresources) | **GET** /silver/ | List Resources |
| [**silverListVersions**](SilverApi.md#silverlistversions) | **GET** /silver/{resource_id}/versions | List Versions |
| [**silverUpdateResource**](SilverApi.md#silverupdateresource) | **PATCH** /silver/{resource_id} | Update Resource |
| [**silverUploadVersion**](SilverApi.md#silveruploadversion) | **POST** /silver/{resource_id}/versions | Upload Version Single |



## silverCreateResource

> CreateResourceResponse silverCreateResource(createResourceRequest)

Create Resource

Creates a new resource in the layer.  Args:         body: A CreateResourceRequest object containing the name, project ID, and                 optional description for the new resource.         loader: The loader instance to use for creating the resource.  Returns:         A CreateResourceResponse containing a success message and the ID of the         newly created resource.

### Example

```ts
import {
  Configuration,
  SilverApi,
} from '';
import type { SilverCreateResourceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SilverApi();

  const body = {
    // CreateResourceRequest
    createResourceRequest: ...,
  } satisfies SilverCreateResourceRequest;

  try {
    const data = await api.silverCreateResource(body);
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


## silverDeleteResource

> MessageResponse silverDeleteResource(resourceId)

Delete Resource

Deletes the specified resource.  Args:         resource_id: The ID of the resource to delete.         loader: The loader instance to use for deleting the resource.  Returns:         A MessageResponse indicating the result of the delete operation.

### Example

```ts
import {
  Configuration,
  SilverApi,
} from '';
import type { SilverDeleteResourceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SilverApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies SilverDeleteResourceRequest;

  try {
    const data = await api.silverDeleteResource(body);
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


## silverDownloadVersion

> any silverDownloadVersion(resourceId, version)

Download Version

Downloads the specified version of the resource as a Parquet file.  Args:         resource_id: The ID of the resource.         version: The version number of the resource.         loader: The loader instance to use for fetching the data.  Returns:         A StreamingResponse containing the Parquet file.

### Example

```ts
import {
  Configuration,
  SilverApi,
} from '';
import type { SilverDownloadVersionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SilverApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies SilverDownloadVersionRequest;

  try {
    const data = await api.silverDownloadVersion(body);
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


## silverGetResource

> MetadataResponse silverGetResource(resourceId)

Get Resource

Retrieves the metadata of the specified resource.  Args:         resource_id: The ID of the resource to retrieve.         loader: The loader instance to use for fetching the metadata.  Returns:         A MetadataResponse object containing the metadata of the resource.

### Example

```ts
import {
  Configuration,
  SilverApi,
} from '';
import type { SilverGetResourceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SilverApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies SilverGetResourceRequest;

  try {
    const data = await api.silverGetResource(body);
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


## silverGetSchema

> SchemaResponse silverGetSchema(resourceId, version)

Get Schema

Returns the schema of the specified version of the resource.  Args:         resource_id: The ID of the resource.         version: The version number of the resource.         loader: The loader instance to use for fetching the data.  Returns:         A SchemaResponse containing the data schema and a sample of the data.

### Example

```ts
import {
  Configuration,
  SilverApi,
} from '';
import type { SilverGetSchemaRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SilverApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies SilverGetSchemaRequest;

  try {
    const data = await api.silverGetSchema(body);
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


## silverListResources

> Array&lt;MetadataResponse&gt; silverListResources()

List Resources

Lists all resources in the layer.  Args:         loader: The loader instance to use for fetching the metadata.  Returns:         A list of MetadataResponse objects containing the metadata of all resources.

### Example

```ts
import {
  Configuration,
  SilverApi,
} from '';
import type { SilverListResourcesRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SilverApi();

  try {
    const data = await api.silverListResources();
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


## silverListVersions

> Array&lt;LineageResponse&gt; silverListVersions(resourceId)

List Versions

Lists all versions of the specified resource along with their lineage information.  Args:         resource_id: The ID of the resource to list versions for.         loader: The loader instance to use for fetching the lineage information.  Returns:         A list of LineageResponse objects representing the versions of the resource.

### Example

```ts
import {
  Configuration,
  SilverApi,
} from '';
import type { SilverListVersionsRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SilverApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies SilverListVersionsRequest;

  try {
    const data = await api.silverListVersions(body);
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


## silverUpdateResource

> MetadataResponse silverUpdateResource(resourceId, updateResourceRequest)

Update Resource

Updates the metadata of the specified resource.  Args:         resource_id: The ID of the resource to update.         body: An UpdateResourceRequest object containing the new name and                 description for the resource.         loader: The loader instance to use for updating the metadata.  Returns:         A MetadataResponse object containing the updated metadata of the resource.

### Example

```ts
import {
  Configuration,
  SilverApi,
} from '';
import type { SilverUpdateResourceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SilverApi();

  const body = {
    // number
    resourceId: 56,
    // UpdateResourceRequest
    updateResourceRequest: ...,
  } satisfies SilverUpdateResourceRequest;

  try {
    const data = await api.silverUpdateResource(body);
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


## silverUploadVersion

> MessageResponse silverUploadVersion(resourceId, fromResourceId, file)

Upload Version Single

Uploads a new version of the resource from a Parquet file.  Args:         resource_id: The ID of the resource to upload a new version for.         file: The uploaded Parquet file containing the new version of the data.         loader: The loader instance to use for uploading the data.         from_resource_id: The ID of the existing resource version that this new                 version is derived from.  Returns:         A MessageResponse indicating the result of the upload operation.

### Example

```ts
import {
  Configuration,
  SilverApi,
} from '';
import type { SilverUploadVersionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new SilverApi();

  const body = {
    // number
    resourceId: 56,
    // number
    fromResourceId: 56,
    // string
    file: file_example,
  } satisfies SilverUploadVersionRequest;

  try {
    const data = await api.silverUploadVersion(body);
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

