# APIEndpointsForInteractingWithTheSilverLayerApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createSourceSilverPost**](APIEndpointsForInteractingWithTheSilverLayerApi.md#createsourcesilverpost) | **POST** /silver/ | Create Source |
| [**deleteSourceSilverSourceIdDelete**](APIEndpointsForInteractingWithTheSilverLayerApi.md#deletesourcesilversourceiddelete) | **DELETE** /silver/{source_id} | Delete Source |
| [**downloadVersionSilverSourceIdVersionsVersionGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#downloadversionsilversourceidversionsversionget) | **GET** /silver/{source_id}/versions/{version} | Download Version |
| [**getSourceSilverSourceIdGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#getsourcesilversourceidget) | **GET** /silver/{source_id} | Get Source |
| [**listSourcesSilverGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#listsourcessilverget) | **GET** /silver/ | List Sources |
| [**listVersionsSilverSourceIdVersionsGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#listversionssilversourceidversionsget) | **GET** /silver/{source_id}/versions | List Versions |
| [**updateSourceSilverSourceIdPatch**](APIEndpointsForInteractingWithTheSilverLayerApi.md#updatesourcesilversourceidpatch) | **PATCH** /silver/{source_id} | Update Source |
| [**uploadVersionSilverSourceIdVersionsPost**](APIEndpointsForInteractingWithTheSilverLayerApi.md#uploadversionsilversourceidversionspost) | **POST** /silver/{source_id}/versions | Upload Version |



## createSourceSilverPost

> any createSourceSilverPost(createSilverSourceRequest)

Create Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { CreateSourceSilverPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // CreateSilverSourceRequest
    createSilverSourceRequest: ...,
  } satisfies CreateSourceSilverPostRequest;

  try {
    const data = await api.createSourceSilverPost(body);
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
| **createSilverSourceRequest** | [CreateSilverSourceRequest](CreateSilverSourceRequest.md) |  | |

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


## deleteSourceSilverSourceIdDelete

> any deleteSourceSilverSourceIdDelete(sourceId)

Delete Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { DeleteSourceSilverSourceIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    sourceId: 56,
  } satisfies DeleteSourceSilverSourceIdDeleteRequest;

  try {
    const data = await api.deleteSourceSilverSourceIdDelete(body);
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


## downloadVersionSilverSourceIdVersionsVersionGet

> any downloadVersionSilverSourceIdVersionsVersionGet(sourceId, version)

Download Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { DownloadVersionSilverSourceIdVersionsVersionGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    sourceId: 56,
    // number
    version: 56,
  } satisfies DownloadVersionSilverSourceIdVersionsVersionGetRequest;

  try {
    const data = await api.downloadVersionSilverSourceIdVersionsVersionGet(body);
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


## getSourceSilverSourceIdGet

> SilverMetadataResponse getSourceSilverSourceIdGet(sourceId)

Get Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { GetSourceSilverSourceIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    sourceId: 56,
  } satisfies GetSourceSilverSourceIdGetRequest;

  try {
    const data = await api.getSourceSilverSourceIdGet(body);
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

[**SilverMetadataResponse**](SilverMetadataResponse.md)

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


## listSourcesSilverGet

> Array&lt;SilverMetadataResponse&gt; listSourcesSilverGet()

List Sources

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { ListSourcesSilverGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  try {
    const data = await api.listSourcesSilverGet();
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

[**Array&lt;SilverMetadataResponse&gt;**](SilverMetadataResponse.md)

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


## listVersionsSilverSourceIdVersionsGet

> Array&lt;SilverLineageResponse&gt; listVersionsSilverSourceIdVersionsGet(sourceId)

List Versions

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { ListVersionsSilverSourceIdVersionsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    sourceId: 56,
  } satisfies ListVersionsSilverSourceIdVersionsGetRequest;

  try {
    const data = await api.listVersionsSilverSourceIdVersionsGet(body);
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

[**Array&lt;SilverLineageResponse&gt;**](SilverLineageResponse.md)

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


## updateSourceSilverSourceIdPatch

> SilverMetadataResponse updateSourceSilverSourceIdPatch(sourceId, updateSilverSourceRequest)

Update Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { UpdateSourceSilverSourceIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    sourceId: 56,
    // UpdateSilverSourceRequest
    updateSilverSourceRequest: ...,
  } satisfies UpdateSourceSilverSourceIdPatchRequest;

  try {
    const data = await api.updateSourceSilverSourceIdPatch(body);
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
| **updateSilverSourceRequest** | [UpdateSilverSourceRequest](UpdateSilverSourceRequest.md) |  | |

### Return type

[**SilverMetadataResponse**](SilverMetadataResponse.md)

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


## uploadVersionSilverSourceIdVersionsPost

> any uploadVersionSilverSourceIdVersionsPost(sourceId, fromSourceId, file)

Upload Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { UploadVersionSilverSourceIdVersionsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    sourceId: 56,
    // number
    fromSourceId: 56,
    // string
    file: file_example,
  } satisfies UploadVersionSilverSourceIdVersionsPostRequest;

  try {
    const data = await api.uploadVersionSilverSourceIdVersionsPost(body);
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
| **fromSourceId** | `number` |  | [Defaults to `undefined`] |
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

