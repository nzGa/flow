import "dart:ui";

/// Locale - (English name, Endonym)
///
/// * You have to include a country if the [Locale.countryCode] is not null.
/// * Your file name must match `languageCode_scriptCode_countryCode` format.
///   `scriptCode` and `countryCode` are optional.
final Map<Locale, (String, String)> supportedLanguages = {
  const Locale("en"): ("English", "English"),
  const Locale("es", "ES"): ("Spanish", "Español"),
  const Locale("pt", "BR"): ("Portuguese (Brazil)", "Português (Brasil)"),
};
