odoo.define("project_vertical_building.stageTreeView", function (require) {
  "use strict";

  const search_panel = require("project_vertical_building.search_panel");

  const ListView = require("web.ListView");
  const viewRegistry = require("web.view_registry");

  var stageTreeView = ListView.extend({}, {
    config: Object.assign({}, ListView.prototype.config, {
      // Controller: DocumentsListController,
      // Model: DocumentsListModel,
      // Renderer: DocumentsListRenderer,
      SearchPanel: search_panel,
    }),
    // searchMenuTypes: ['filter', 'favorite'],
  });

  viewRegistry.add("vertical_stage_tree", stageTreeView);

  return stageTreeView;
});
