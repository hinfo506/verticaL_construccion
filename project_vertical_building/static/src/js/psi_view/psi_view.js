/** @odoo-module **/
/** SEE https://dgoguerra.github.io/bootstrap-menu/demos.html FOR MORE INFO */
import { registry } from "@web/core/registry";
import { Layout } from "@web/views/layout";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model, useModel } from "@web/views/helpers/model";
const { useSubEnv } = owl.hooks;

class ProjectStageItemModel extends Model {
  static services = ["orm"];

  setup(params, { orm }) {
    this.model = params.resModel;
    console.log(this.model); //vertical.stage
    this.orm = orm;
    this.keepLast = new KeepLast();
  }

  async load(params) {
    this.data = await this.keepLast.add(
      this.orm.searchRead(this.model, params.domain, [], { limit: 100 })
    );
    this.notify();
  }
}

class ProjectStageItemView extends owl.Component {
  setup() {
    this.model = useModel(ProjectStageItemModel, {
      resModel: this.props.resModel,
      domain: this.props.domain,
    });
    let searchModel = this.env.searchModel;
    searchModel.display = {
      controlPanel: false,
      searchPanel: false,
    };
    useSubEnv({ searchModel: searchModel });
  }
  mounted(){
    const self = this;
    // do something
    const menu = new BootstrapMenu(".context-menu-item", {
      /* a function to know which element was the context menu opened on,
       * given the selected DOM element. When this function is defined,
       * every user-defined action callback receives its return value as
       * an argument. */
      fetchElementData: function ($elem) {
        const record_id = $elem.data("id");
        return self.model.data[0];
      },
      actions: [
        {
          name: "Edit name",
          onClick: function (record) {
            alert(record.id);
          },
        },
        {
          name: "Edit description",
          onClick: function (record) {
            alert(record.id);
          },
        },
      ],
    });
   }
}

ProjectStageItemView.type = "project_stage_item";
ProjectStageItemView.display_name = "ProjectStageItemView";
ProjectStageItemView.icon = "fa-heart";
ProjectStageItemView.multiRecord = true;
ProjectStageItemView.searchMenuTypes = ["filter", "favorite"];
ProjectStageItemView.components = { Layout };
ProjectStageItemView.template = "project_vertical_view.Layout";

registry.category("views").add("project_stage_item", ProjectStageItemView);
