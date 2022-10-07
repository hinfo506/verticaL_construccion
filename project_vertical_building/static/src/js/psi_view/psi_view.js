/** @odoo-module **/
/** SEE https://dgoguerra.github.io/bootstrap-menu/demos.html FOR MORE INFO */
import { registry } from "@web/core/registry";
import { Layout } from "@web/views/layout";
import { KeepLast } from "@web/core/utils/concurrency";
import { Model, useModel } from "@web/views/helpers/model";
const { useSubEnv, useState } = owl.hooks;

const FIELDS = ["id", "name", "parent_id", "project_id", "numero_fase", "fecha_finalizacion", "cantidad", "total", "type_stage_id"];
// const FIELDS = [];

class ProjectStageItemModel extends Model {
  static services = ["orm"];

  setup(params, { orm }) {
    this.model = params.resModel;
    this.orm = orm;
    this.keepLast = new KeepLast();
  }

  async load(params) {
    const self = this;
    const domain = params.domain;
    if ("project_id" in params.context) {
      domain.push(["project_id", "in", params.context.project_id]);
    }
    this.rawData = await self.keepLast.add(
      this.orm.searchRead(this.model, domain, FIELDS, { limit: 1000 })
    )
    const projectStageItemData = _.map(
      _.uniq(
        _.map(self.rawData, (stage) => stage.project_id),
        _.iteratee((project) => project[0])
      ),
      (project_id) => {
        return {
          id: false,
          project_id: project_id,
          vertical_stage_ids: _.filter(
            self.rawData,
            (stage) =>
              stage.project_id[0] === project_id[0] && stage.parent_id === false
          ),
        };
      }
    );
    projectStageItemData.forEach((projectStageItem) =>
      projectStageItem.vertical_stage_ids.forEach((stage) =>
        self._create_stages_tree(stage)
      )
    );
    this.projectStageItemData = projectStageItemData;
    this.notify();
  }

  async load_items_for_stage(stage_id){
    const ITEM_FIELDS = ['id', 'date', 'job_type', 'color_item', 'product_id', 'product_qty', 'reference', 'cost_price', 'subtotal_item_capitulo'];
    const stageItems = await this.keepLast.add(
      this.orm.searchRead('vertical.item', [['vertical_stage_id','=',stage_id]], ITEM_FIELDS, { limit: 1000 })
    );
    console.log(stageItems);
    const index = _.findIndex(this.rawData, (stage) => stage.id === stage_id);
    this.rawData[index]['item_ids'] = stageItems;
    this.notify();
  }

  _create_stages_tree(stagesTree) {
    const self = this;
    stagesTree.vertical_stage_ids = _.filter(
      self.rawData,
      (stage) => stage.parent_id[0] === stagesTree.id
    );
    _.map(stagesTree.vertical_stage_ids, (currentStage) =>
      self._create_stages_tree(currentStage)
    );
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
      controlPanel: true,
      searchPanel: false,
    };
    useSubEnv({ searchModel: searchModel });

    this.state = useState({
      active: {},
      expanded: {},
      expandedStages: [],
      activeStages: [],
      selectedStage: 0,
      stageObj: {},
    });
    this.scrollTop = 0;
    this.hasImportedState = false;

    this.importState(this.props.importedState);
  }

  async willStart() {
    const self = this;
    // This is ugly, fix it with promises
    // const handleModelLoaded = () => {
    //   if (!self.model.rawData){
    //     setTimeout(() => {
    //       handleModelLoaded();
    //     }, 100);
    //   } else {
    //     self.expandDefaultValue();
    //   }
    // };
    // handleModelLoaded();
  }
  mounted() {
    const self = this;
    // do something
    const menu = new BootstrapMenu(".context-menu-item", {
      /* a function to know which element was the context menu opened on,
       * given the selected DOM element. When this function is defined,
       * every user-defined action callback receives its return value as
       * an argument. */
      fetchElementData: function ($elem) {
        const record_id = $elem.data("id");
        return _.find(self.model.rawData, (stage) => stage.id === record_id);
      },
      /* group actions by their id to make use of separators between
      * them in the context menu. Actions not added to any group with
      * this option will appear in a default group of their own. */
      // actionsGroups: [
      //   ['setEditable', 'setUneditable' ],
      //   ['deleteRow']
      // ],
      actions: {
        editName: {
          name: 'Editar Fase',
          iconClass: 'fa-pencil',
          onClick: function(row) {
            alert("'Edit name' clicked on '" + row.name + "'");
          },
          isEnabled: function(row) {
            return row.isEditable;
          }
        },
        createSubStage: {
          name: 'Crear SubFase',
          iconClass: 'fa-pencil',
          onClick: function(row) {
            alert("'Edit description' clicked on '" + row.name + "'");
          },
        },
        uploadStandar: {
          name: 'Subir Estandar',
          iconClass: 'fa-unlock',
          onClick: function(row) {
            alert("'Set editable' clicked on '" + row.name + "'");
          },
          // isShown: function(row) {
          //   return !row.isEditable;
          // }
        },
        sendToPurchases: {
          name: 'Enviar a Compra',
          iconClass: 'fa-lock',
          onClick: function(row) {
            alert("'Set uneditable' clicked on '" + row.name + "'");
          },
          // isShown: function(row) {
          //   return row.isEditable;
          // }
        },
        globalPurchase: {
          name: 'Compra Global',
          iconClass: 'fa-trash-o',
          onClick: function(row) {
            alert("'Delete row' clicked on '" + row.name + "'");
          },
        },
        deleteStage: {
          name: 'Borrar Fase',
          iconClass: 'fa-trash-o',
          onClick: function(row) {
            alert("'Delete row' clicked on '" + row.name + "'");
          },
          // isEnabled: function(row) {
          //   return row.isEditable && row.isRemovable;
          // }
        }
      }
    });
  }
  //---------------------------------------------------------------------
  // Public
  //---------------------------------------------------------------------

  async toggleStage(stage_id){
    const stage = _.find(this.model.rawData, (stage) => stage.id === stage_id);
    if(stage.vertical_stage_ids.length > 0){
      const indexOfActiveStage = this.state.activeStages.indexOf(stage_id);
      if(indexOfActiveStage >= 0){
        //remove it
        this.state.activeStages = _.without(this.state.activeStages, stage_id);
      }else{
        //put it
        this.state.activeStages.push(stage_id);
      }
    }
    else{
      await this.model.load_items_for_stage(stage_id);
    }
    if(this.state.selectedStage !== stage_id){
      this.state.selectedStage = stage_id;
      this.state.stageObj = _.find(this.model.rawData, (stage) => stage.id === stage_id);
    }
  }

  onRowClicked(stage_id){
    const viewRegistry = registry.category("views");
    console.log(viewRegistry);
    const stage = _.find(this.model.rawData, (stage) => stage.id === stage_id);
    const action = {
      type: "ir.actions.act_window",
      name: stage.name,
      res_model: 'vertical.stage',
      view_mode: "form",
      target: "current",
      res_id: stage_id,
      // views: ['form'],
      context: {},
      domain: [['id','=',stage_id]]
    };
    console.log('JSON.stringify(action): ');
    console.log(JSON.stringify(action));
    if (stage_id){
      // env.services.action.doAction(action.actionID, { clearBreadcrumbs: true });
      // this.env.services.action.doAction(action, {viewType: 'form'});
      this.env.services.action.switchView("form", {resId: stage_id});
    }
  }

  exportState() {
    const exported = {
      expanded: this.state.expanded,
      scrollTop: this.el.scrollTop,
      stageTree: this.state.stageTree,
    };
    return JSON.stringify(exported);
  }

  importState(stringifiedState) {
    this.hasImportedState = Boolean(stringifiedState);
    if (this.hasImportedState) {
      const state = JSON.parse(stringifiedState);
      this.state.expanded = state.expanded;
      this.scrollTop = state.scrollTop;
    }
  }
  //---------------------------------------------------------------------
  // Protected
  //---------------------------------------------------------------------

  /**
   * Expands category values holding the default value of a category.
   */
  expandDefaultValue() {
    const self = this;
    if (this.hasImportedState) {
      return;
    }

  }
  /**
   * @param {Object} category
   * @param {number} stage_id
   * @returns {number[]} list of ids of the ancestors of the given value in
   *   the given category.
   */
  getAncestorValueIds(stage, stage_id) {
    // const { parent_id } = stage.values.get(stage_id);
    const self = this;
    const { parent_id } = _.find(self.model.data, (stage) => stage.parent_id[0] === stage_id);
    return parent_id[0] ? [...this.getAncestorValueIds(stage, parent_id[0]), parent_id[0]] : [];
  }
}

// ProjectStageItemView.props = {
//   importedState: { type: String, optional: true },
// };
ProjectStageItemView.type = "project_stage_item";
ProjectStageItemView.display_name = "ProjectStageItemView";
ProjectStageItemView.icon = "fa-sitemap";
ProjectStageItemView.multiRecord = true;
ProjectStageItemView.searchMenuTypes = ["filter", "favorite"];
ProjectStageItemView.components = { Layout };
ProjectStageItemView.template = "project_vertical_view.Layout";
ProjectStageItemView.subTemplates = {
  project: "project_vertical_view.Project",
  stage: "project_vertical_view.Stage",
};

registry.category("views").add("project_stage_item", ProjectStageItemView);

/**
 listrenderer.js
  _onRowClicked: function (ev) {
    // The special_click property explicitely allow events to bubble all
    // the way up to bootstrap's level rather than being stopped earlier.
    if (!ev.target.closest('.o_list_record_selector') && !$(ev.target).prop('special_click') && !this.no_open) {
        var id = $(ev.currentTarget).data('id');
        if (id) {
            this.trigger_up('open_record', { id: id, target: ev.target });
        }
    }
},
 */


/**
 * abstract
     * When an Odoo event arrives requesting a record to be opened, this method
     * gets the res_id, and request a switch view in the appropriate mode
     *
     * Note: this method seems wrong, it relies on the model being a basic model,
     * to get the res_id.  It should receive the res_id in the event data
     * @todo move this to basic controller?
     *
     * @private
     * @param {OdooEvent} ev
     * @param {number} ev.data.id The local model ID for the record to be
     *   opened
     * @param {string} [ev.data.mode='readonly']
     */
 /*_onOpenRecord: function (ev) {
  ev.stopPropagation();
  var record = this.model.get(ev.data.id, {raw: true});
  this.trigger_up('switch_view', {
      view_type: 'form',
      res_id: record.res_id,
      mode: ev.data.mode || 'readonly',
      model: this.modelName,
  });
},*/