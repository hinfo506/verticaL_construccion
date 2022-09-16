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
    // console.log(this.model); //vertical.stage
    this.orm = orm;
    this.keepLast = new KeepLast();
  }

  async load(params) {
    const self = this;
    const domain = params.domain;
    if ('project_id' in params.context){
      domain.push(['project_id', 'in', params.context.project_id]);
    }
    const rawData = await this.keepLast.add(
      this.orm.searchRead(this.model, domain, [], { limit: 1000 })
    );
    this.rawData = rawData;
    const projectStageItemData = _.map(_.uniq(_.map(rawData, (item) => item.project_id), _.iteratee((project => project[0]))), (project_id) => {return {
      'id': false,
      'project_id': project_id,
      'vertical_stage_ids': _.filter(rawData, (stage) => stage.project_id[0] === project_id[0] && stage.parent_id === false),
    }});
    projectStageItemData.forEach(
      (projectStageItem) => projectStageItem.vertical_stage_ids.forEach(
        (stage) => self._create_stages_tree(stage)));
    console.log(projectStageItemData);
    this.data = rawData;
    this.notify();
  }

  _create_stages_tree(stagesTree){
    const self = this;
    stagesTree.vertical_stage_ids = _.filter(self.rawData, (stage) => stage.parent_id[0] === stagesTree.id);
    _.map(stagesTree.vertical_stage_ids, (currentStage) => self._create_stages_tree(currentStage));
  }

}

class ProjectStageItemView extends owl.Component {
  setup() {
    this.model = useModel(ProjectStageItemModel, {
      resModel: this.props.resModel,
      domain: this.props.domain,
    });
    let searchModel = this.env.searchModel;
    // console.log(this);
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
ProjectStageItemView.subTemplates = {
  project: "project_vertical_view.Project",
  stage: "project_vertical_view.Stage",
};


registry.category("views").add("project_stage_item", ProjectStageItemView);
