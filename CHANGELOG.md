# Changelog

## Notes on versioning

- Adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html), (Major.Minor.Patch).

- Each release may affect, app, server, or both. Version numbers will be updated in step in both, even if no changes present in one. Release notes/this changelog will indicate which repository (app or server) contains the changes.

- All releases within the same Major version should be compatible. Using the same version of both is recommended.

## v0.2.0 (2023-12-13)

Affects [DocumentHarbor Server](https://github.com/tyson-01/DocumentHarbor_Server) only

### Added

- Experimental feature: automatic document extraction from images. Must be enabled in the config.ini file, this feature will effect the "Create PDF" and "Merge PDF" modes. The server will now identify the edges of the document in the image, realign the document to a perfect rectangle to account for small angles in the image capturing process, and crops the image to only contain the document. For best results, place documents on solid contrasting background. Does not handle things like metal coils from coiled notebook well. If some of the documents in your final pdf are not extracted, it failed on those images.

## v0.1.1 (2023-12-08)

Affects [DocumentHarbor App](https://github.com/tyson-01/DocumentHarbor_App) only

### Fixed

- Allows newer android devices to communicate to server over http.

## v0.1.0 (2023-11-27)

Affects [DocumentHarbor App](https://github.com/tyson-01/DocumentHarbor_App) and [DocumentHarbor Server](https://github.com/tyson-01/DocumentHarbor_Server)

### Added

- Basic functionality of app and server.

- Three modes of operation:

- Leave as images: all pictures taken are stored as is with sequential names to retain order.

- Create PDFs: all pictures converted to PDFs with sequential names to retain order.

- Merge PDFs: all pictures converted to PDFs and appended into one pdf file.