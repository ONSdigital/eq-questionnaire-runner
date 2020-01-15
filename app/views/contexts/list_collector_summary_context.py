from flask import url_for

from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.list_collector_context import ListCollectorContext
from app.views.contexts.context import Context


class ListCollectorSummaryContext(Context):
    def build_view_context(self, current_location):

        block = self._schema.get_block(current_location.block_id)

        return {
            "summary": {
                "title": block["title"],
                "list_summaries": self.get_list_summaries(current_location),
            }
        }

    def get_list_summaries(self, current_location):
        section = self._schema.get_section(current_location.section_id)
        visible_list_collector_blocks = self._schema.get_visible_list_blocks_for_section(
            section
        )
        section_path = self._router.section_routing_path(
            section["id"], current_location.list_item_id
        )
        section_path_block_ids = [location.block_id for location in section_path]
        list_summaries = []

        for list_collector_block in visible_list_collector_blocks:
            add_link = url_for(
                "questionnaire.block",
                list_name=list_collector_block["for_list"],
                block_id=list_collector_block["add_block"]["id"],
                return_to=current_location.block_id,
            )

            if list_collector_block["id"] not in section_path_block_ids:
                driving_question_block = QuestionnaireSchema.get_driving_question_for_list(
                    section, list_collector_block["for_list"]
                )

                if driving_question_block:
                    add_link = url_for(
                        "questionnaire.block", block_id=driving_question_block["id"]
                    )

            rendered_summary = self._placeholder_renderer.render(
                list_collector_block["summary"], current_location.list_item_id
            )

            list_context = ListCollectorContext(
                self._language,
                self._schema,
                self._answer_store,
                self._list_store,
                self._progress_store,
                self._metadata,
            )

            list_items = list_context.build_list_items_summary_context(
                list_collector_block, current_location.block_id
            )

            list_summary = {
                "title": rendered_summary["title"],
                "add_link": add_link,
                "add_link_text": rendered_summary["add_link_text"],
                "empty_list_text": rendered_summary["empty_list_text"],
                "list_name": list_collector_block["for_list"],
            }

            if list_items:
                list_summary["list"] = {"list_items": list_items, "editable": True}

            list_summaries.append(list_summary)

        return list_summaries
