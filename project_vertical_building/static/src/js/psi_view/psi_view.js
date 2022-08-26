/** @odoo-module **/
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
      useSubEnv({searchModel: searchModel});
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
