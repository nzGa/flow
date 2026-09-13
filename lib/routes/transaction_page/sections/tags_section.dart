import "package:flow/entity/transaction_tag.dart";
import "package:flow/l10n/extensions.dart";
import "package:flow/prefs/local_preferences.dart";
import "package:flow/routes/transaction_page/section.dart";
import "package:flow/widgets/general/frame.dart";
import "package:flow/widgets/transaction_tag_add_chip.dart";
import "package:flow/widgets/transaction_tag_chip.dart";
import "package:flutter/material.dart";
import "package:flutter/services.dart";

class TagsSection extends StatelessWidget {
  final List<TransactionTag>? selectedTags;
  final VoidCallback selectTags;

  const TagsSection({
    super.key,
    this.selectedTags,
    required this.selectTags,
  });

  @override
  Widget build(BuildContext context) {
    return Section(
      title: "transaction.tags".t(context),
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        child: Frame(
          child: Padding(
            padding: const EdgeInsets.only(top: 8.0),
            child: Align(
              alignment: AlignmentDirectional.topStart,
              child: Wrap(
                spacing: 12.0,
                runSpacing: 8.0,
                children: [
                  TransactionTagAddChip(
                    onPressed: selectTags,
                    title: "transaction.tags.add".t(context),
                  ),
                  ...?selectedTags?.map(
                    (tag) => IgnorePointer(
                      child: TransactionTagChip(tag: tag, selected: true),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        onTap: () {
          if (LocalPreferences().enableHapticFeedback.get()) {
            HapticFeedback.lightImpact();
          }

          selectTags();
        },
      ),
    );
  }
}
