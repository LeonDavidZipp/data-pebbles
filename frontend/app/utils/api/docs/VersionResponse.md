
# VersionResponse


## Properties

Name | Type
------------ | -------------
`id` | number
`source_id` | number
`version` | number
`status` | string
`s3_key` | string
`created_at` | string
`updated_at` | string

## Example

```typescript
import type { VersionResponse } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "source_id": null,
  "version": null,
  "status": null,
  "s3_key": null,
  "created_at": null,
  "updated_at": null,
} satisfies VersionResponse

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as VersionResponse
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


