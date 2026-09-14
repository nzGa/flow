# ![Flow logo](logo@32.png) simpleFlow

Personal, offline-first expense tracker. This is a **modified version** of
[Flow](https://github.com/flow-mn/flow) (September 2026). It remains free
software under the [GNU General Public License v3](./LICENSE).

Original copyright: Copyright (C) 2024 Batmend Ganbaatar and authors of Flow.
See [NOTICE](./NOTICE) for attribution and a summary of what changed.

This is not the Flow app on the App Store or Google Play. The original authors
are not responsible for this project.

**Repository:** [github.com/nzGa/simpleFlow](https://github.com/nzGa/simpleFlow)

## What it is

Accounts, transactions, categories, and spending stats. Build from source
(macOS and Linux work; Windows is untested). Web is not supported (ObjectBox).

Compared with upstream Flow, simpleFlow drops Eny, in-app support/community
and IAP, maps and geo tagging, attachments / camera / Markdown notes, tags and
budgets from the UI, OS scheduled notifications, store-publish workflows, and
the in-app trash and money-format preferences. Amounts are always shown in
full with ISO codes (`ARS`, `BRL`, `EUR`, `USD`), never abbreviated and never
as `$` / `€`. Existing backup data for removed features is still imported.

## Features

* Day-to-day tracking with a simple UI
* Accounts in ARS, BRL, EUR, or USD
* Categories and spending stats
* Fully offline[^1]
* Data stays on device
  * No trackers, no analytics
  * Recoverable backups (ZIP/JSON)
  * Export CSV and PDFs
  * Periodic auto-backups to iCloud (Apple platforms)
* UI languages: English, Spanish, Portuguese (Brazil)[^2]
* [URI-based automation](#uri-based-automation)

## URI-based automation

You can add one or more transactions using `flow-mn` scheme URIs (unchanged
from upstream).

See the [JSON Schema in `schemas/`](./schemas/programmable-object.json).
Currency comes from the account; it cannot be set on the URI.

### Adding a single transaction

Properties go in query params.

```json
{
  "title": "Tous les jours",
  "amount": 42000.00
}
```

turns into:

```plain
flow-mn:///transaction/new?title=Tous+les+jours&amount=42000.00
```

### Adding multiple transactions

Pass a stringified JSON object as the `json` query param.

```json
{
  "t": [
    {
      "title": "Fresh blueberry piece",
      "amount": "13000.00",
      "transactionDate": "2011-12-05",
      "category": "Food",
      "accountUuid": "faa6d523-277f-46af-9493-67768e5b48ab"
    },
    {
      "title": "Caffe Mocha ice",
      "amount": "10000.00",
      "transactionDate": "2011-12-05",
      "category": "Drinks"
    }
  ]
}
```

## Development

Personal project. See [CONTRIBUTING.md](./CONTRIBUTING.md) if you still want
to open a pull request.

### Prerequisites

* [Flutter](https://flutter.dev/) (latest stable)
* JDK 11 or later to build for Android
* [Xcode](https://developer.apple.com/xcode/) to build for iOS/macOS

Desktop builds need the same native deps as Flutter. See
<https://docs.flutter.dev/platform-integration>.

### Testing

Install ObjectBox dynamic libraries first[^3]:

```sh
bash <(curl -s https://raw.githubusercontent.com/objectbox/objectbox-dart/main/install.sh)
```

Then: `flutter test`

## Original Flow

Upstream: [flow-mn/flow](https://github.com/flow-mn/flow).
To support the original maintainer:
[buymeacoffee.com/sadespresso](https://buymeacoffee.com/sadespresso).

Thanks to everyone who contributed translations, testing, and code to Flow.

[^1]: Internet is only needed to download exchange rates when you use more
than one currency.

[^2]: Portuguese uses English app strings until a full translation exists.
Material widgets can still follow the system Portuguese locale.

[^3]: Confirm the current install steps at
<https://docs.objectbox.io/getting-started#add-objectbox-to-your-project>
(choose Flutter).
