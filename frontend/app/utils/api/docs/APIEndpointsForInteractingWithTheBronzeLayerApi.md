# APIEndpointsForInteractingWithTheBronzeLayerApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**activateVersionBronzeSourceIdVersionsVersionPatch**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#activateversionbronzesourceidversionsversionpatch) | **PATCH** /bronze/{source_id}/versions/{version} | Activate Version |
| [**createSourceBronzePost**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#createsourcebronzepost) | **POST** /bronze/ | Create Source |
| [**deleteSourceBronzeSourceIdDelete**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#deletesourcebronzesourceiddelete) | **DELETE** /bronze/{source_id} | Delete Source |
| [**deleteVersionBronzeSourceIdVersionsVersionDelete**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#deleteversionbronzesourceidversionsversiondelete) | **DELETE** /bronze/{source_id}/versions/{version} | Delete Version |
| [**downloadVersionBronzeSourceIdVersionsVersionGet**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#downloadversionbronzesourceidversionsversionget) | **GET** /bronze/{source_id}/versions/{version} | Download Version |
| [**getSourceBronzeSourceIdGet**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#getsourcebronzesourceidget) | **GET** /bronze/{source_id} | Get Source |
| [**listSourcesBronzeGet**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#listsourcesbronzeget) | **GET** /bronze/ | List Sources |
| [**listVersionsBronzeSourceIdVersionsGet**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#listversionsbronzesourceidversionsget) | **GET** /bronze/{source_id}/versions | List Versions |
| [**updateSourceBronzeSourceIdPatch**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#updatesourcebronzesourceidpatch) | **PATCH** /bronze/{source_id} | Update Source |
| [**uploadVersionBronzeSourceIdVersionsPost**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#uploadversionbronzesourceidversionspost) | **POST** /bronze/{source_id}/versions | Upload Version |



## activateVersionBronzeSourceIdVersionsVersionPatch

> any activateVersionBronzeSourceIdVersionsVersionPatch(sourceId, version)

Activate Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { ActivateVersionBronzeSourceIdVersionsVersionPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    sourceId: 56,
    // number
    version: 56,
  } satisfies ActivateVersionBronzeSourceIdVersionsVersionPatchRequest;

  try {
    const data = await api.activateVersionBronzeSourceIdVersionsVersionPatch(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |
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


## createSourceBronzePost

> any createSourceBronzePost(createSourceRequest)

Create Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { CreateSourceBronzePostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // CreateSourceRequest
    createSourceRequest: ...,
  } satisfies CreateSourceBronzePostRequest;

  try {
    const data = await api.createSourceBronzePost(body);
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
| **createSourceRequest** | [CreateSourceRequest](CreateSourceRequest.md) |  | |

### Return type

**any**

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


## deleteSourceBronzeSourceIdDelete

> any deleteSourceBronzeSourceIdDelete(sourceId)

Delete Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { DeleteSourceBronzeSourceIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    sourceId: 56,
  } satisfies DeleteSourceBronzeSourceIdDeleteRequest;

  try {
    const data = await api.deleteSourceBronzeSourceIdDelete(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |

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


## deleteVersionBronzeSourceIdVersionsVersionDelete

> any deleteVersionBronzeSourceIdVersionsVersionDelete(sourceId, version)

Delete Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { DeleteVersionBronzeSourceIdVersionsVersionDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    sourceId: 56,
    // number
    version: 56,
  } satisfies DeleteVersionBronzeSourceIdVersionsVersionDeleteRequest;

  try {
    const data = await api.deleteVersionBronzeSourceIdVersionsVersionDelete(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |
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


## downloadVersionBronzeSourceIdVersionsVersionGet

> any downloadVersionBronzeSourceIdVersionsVersionGet(sourceId, version)

Download Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { DownloadVersionBronzeSourceIdVersionsVersionGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    sourceId: 56,
    // number
    version: 56,
  } satisfies DownloadVersionBronzeSourceIdVersionsVersionGetRequest;

  try {
    const data = await api.downloadVersionBronzeSourceIdVersionsVersionGet(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |
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


## getSourceBronzeSourceIdGet

> MetadataResponse getSourceBronzeSourceIdGet(sourceId)

Get Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { GetSourceBronzeSourceIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    sourceId: 56,
  } satisfies GetSourceBronzeSourceIdGetRequest;

  try {
    const data = await api.getSourceBronzeSourceIdGet(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |

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


## listSourcesBronzeGet

> Array&lt;MetadataResponse&gt; listSourcesBronzeGet()

List Sources

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { ListSourcesBronzeGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  try {
    const data = await api.listSourcesBronzeGet();
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


## listVersionsBronzeSourceIdVersionsGet

> Array&lt;VersionResponse&gt; listVersionsBronzeSourceIdVersionsGet(sourceId)

List Versions

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { ListVersionsBronzeSourceIdVersionsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    sourceId: 56,
  } satisfies ListVersionsBronzeSourceIdVersionsGetRequest;

  try {
    const data = await api.listVersionsBronzeSourceIdVersionsGet(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**Array&lt;VersionResponse&gt;**](VersionResponse.md)

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


## updateSourceBronzeSourceIdPatch

> MetadataResponse updateSourceBronzeSourceIdPatch(sourceId, updateSourceRequest)

Update Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { UpdateSourceBronzeSourceIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    sourceId: 56,
    // UpdateSourceRequest
    updateSourceRequest: ...,
  } satisfies UpdateSourceBronzeSourceIdPatchRequest;

  try {
    const data = await api.updateSourceBronzeSourceIdPatch(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |
| **updateSourceRequest** | [UpdateSourceRequest](UpdateSourceRequest.md) |  | |

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


## uploadVersionBronzeSourceIdVersionsPost

> any uploadVersionBronzeSourceIdVersionsPost(sourceId, file)

Upload Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { UploadVersionBronzeSourceIdVersionsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    sourceId: 56,
    // string
    file: file_example,
  } satisfies UploadVersionBronzeSourceIdVersionsPostRequest;

  try {
    const data = await api.uploadVersionBronzeSourceIdVersionsPost(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |
| **file** | `string` |  | [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `multipart/form-data`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

