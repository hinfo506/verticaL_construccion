odoo.define(
  "project_vertical_building.vertical_search_panel_model_extension",
  function (require) {
    "use strict";

    const ActionModel = require("web.ActionModel");
    const SearchPanelModelExtension = require("web.searchPanelModelExtension");
    const pyUtils = require("web.py_utils");

    const DEFAULT_LIMIT = 200;
    let nextSectionId = 1;

    //     // Helpers
    //     const isFolderCategory = (s) => s.type === "category" && s.fieldName === "folder_id";
    //     const isTagFilter = (s) => s.type === "filter" && s.fieldName === "tag_ids";

    class vertical_search_panel_model_extension extends SearchPanelModelExtension {

      async _fetchCategories(categories) {
        //No nos interesan las categorías, siempre será 1 y viene en el contexto, es el proyecto seleccionado.
        await Promise.all(
          categories.map(async (category) => {
            const domain = [
              ["project_id", "=", this.config.context.project_id],
            ];
            const fields = ["id", "display_name", "parent_id"];
            const results = await this.env.services.rpc({
              method: "search_read",
              model: "vertical.stage",
              args: [domain, fields],
              kwargs: {
                context: this.config.context,
              },
            });
            this._createCategoryTree(category.id, {
              parent_field: "parent_id",
              values: results.map((result) => {
                return {
                  ...result,
                  parent_id: result.parent_id ? result.parent_id[0] : false,
                };
              }),
            });
          })
        );
      }

      _getCategoryDomain(excludedCategoryId) {
        const domain = [];
        for (const category of this.categories) {
          if (category.id === excludedCategoryId) {
            continue;
          }
          if (!category.activeValueId) {
            domain.push(['parent_id', '=', false]);
            continue;
          }
          domain.push(['parent_id', '=', category.activeValueId]);
        }
        return domain;
      }

      _createSectionsFromArch() {
        let hasCategoryWithCounters = false;
        let hasFilterWithDomain = false;
        this.config.archNodes.forEach(({ attrs, tag }, index) => {
          if (tag !== "field" || attrs.invisible === "1") {
            return;
          }
          const type = attrs.select === "multi" ? "filter" : "category";
          const section = {
            color: attrs.color,
            description: attrs.string || this.config.fields[attrs.name].string,
            enableCounters: !!pyUtils.py_eval(attrs.enable_counters || "0"),
            expand: !!pyUtils.py_eval(attrs.expand || "0"),
            fieldName: attrs.name,
            icon: attrs.icon,
            id: nextSectionId++,
            index,
            limit: pyUtils.py_eval(attrs.limit || String(DEFAULT_LIMIT)),
            type,
            values: new Map(),
          };
          if (type === "category") {
            section.activeValueId = this.defaultValues[attrs.name];
            section.icon = section.icon || "fa-folder";
            section.hierarchize = !!pyUtils.py_eval(attrs.hierarchize || "1");
            section.values.set(false, {
              childrenIds: [],
              display_name:
                this.config.context.searchpanel_project_building_name ||
                this.env._t("Building Project"),
              id: false,
              bold: true,
              parentId: false,
            });
            hasCategoryWithCounters =
              hasCategoryWithCounters || section.enableCounters;
          } else {
            section.domain = attrs.domain || "[]";
            section.groupBy = attrs.groupby;
            section.icon = section.icon || "fa-filter";
            hasFilterWithDomain =
              hasFilterWithDomain || section.domain !== "[]";
          }
          this.state.sections.set(section.id, section);
        });
        /**
         * Category counters are automatically disabled if a filter domain is found
         * to avoid inconsistencies with the counters. The underlying problem could
         * actually be solved by reworking the search panel and the way the
         * counters are computed, though this is not the current priority
         * considering the time it would take, hence this quick "fix".
         */
        if (hasCategoryWithCounters && hasFilterWithDomain) {
          // If incompatibilities are found -> disables all category counters
          for (const category of this.categories) {
            category.enableCounters = false;
          }
          // ... and triggers a warning
          console.warn(
            "Warning: categories with counters are incompatible with filters having a domain attribute.",
            "All category counters have been disabled to avoid inconsistencies."
          );
        }
      }
    }

    ActionModel.registry.add(
      "VerticalSearchPanelMO",
      vertical_search_panel_model_extension,
      30
    );

    return vertical_search_panel_model_extension;
  }
);
