odoo.define("project_vertical_building.search_panel", function (require) {
  "use strict";

  const SearchPanel = require("web.searchPanel"); //FOR LEGACY
  // const { SearchPanel } = require("@web/search/search_panel/search_panel"); //FOR NEW OWL

  class search_panel extends SearchPanel {
  }
  search_panel.modelExtension = "VerticalSearchPanelMO";

  search_panel.template = "project_vertical_building.Legacy.SearchPanel";

  return search_panel;
});
