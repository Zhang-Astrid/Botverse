<template>
  <div class="mybot-container">
    <el-button type="primary" @click="addRobot" v-if="is_current">创建新机器人</el-button>
    <el-table :data="robots" style="width: 100%">
      <el-table-column prop="id" label="MID"></el-table-column>
      <el-table-column prop="name" label="名称"></el-table-column>
      <el-table-column prop="type" label="类型"></el-table-column>
      <el-table-column prop="prompt" label="提示词"></el-table-column>
      <el-table-column label="操作" width="180" >
        <template #default="scope">
          <el-button @click="showDetail(scope.row.id)" type="primary" size="small">详情</el-button>
          <el-button @click="deleteRobot(scope.row.id)" type="primary" size="small" v-if="is_current">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="添加机器人" >
      <el-form ref="dataForm" :model="dataForm" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="dataForm.name"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="dataForm.type" placeholder="请选择">
            <el-option label="gpt-3.5-turbo" value="gpt-3.5-turbo"></el-option>
            <el-option label="gpt-4o" value="gpt-4o"></el-option>
            <el-option label="gpt-4o-mini" value="gpt-4o-mini"></el-option>
            <el-option label="dall-e-3" value="dall-e-3"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="提示词">
          <el-select v-model="selectedOption" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          <el-input
            v-if="selectedOption === 'other'"
            v-model="customPrompt"
            placeholder="请输入自定义提示词">
          </el-input>
        </el-form-item>
        <el-form-item label="介绍">
          <el-input v-model="dataForm.content"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>

import UserInfo from "@/views/user/components/UserInfo.vue";
import axios from "axios";
import { mapGetters } from 'vuex';
export default {
  computed: {
    ...mapGetters(['getSharedData']),
  },
  data() {
    return {
      selectedOption: '', // 用于绑定选中的选项
      customPrompt: '', // 用于绑定自定义输入框的值
      options: [ // 预设的选项
       { value: 'creative_writing', label: '创意写作' },
        { value: 'life_helper', label: '生活帮手' },
        { value: 'inspiration_planning', label: '灵感策划' },
        { value: 'emotional_communication', label: '情感交流' },
        { value: 'character_dialogue', label: '人物对话' },
        { value: 'business_analysis', label: '商业分析' },
        { value: 'education_training', label: '教育培训' },
        { value: 'job_hunter', label: '求职招聘' },
        { value: 'gourmet_window', label: '美食之窗' },
        { value: 'popular_qa', label: '热门问答' },
        { value: 'functional_writing', label: '功能写作' },
        { value: 'popular_holidays', label: '热门节日' },
        { value: 'programming_assistance', label: '编程辅助' },
        { value: 'travel_vacation', label: '旅行度假' },
        { value: 'data_analysis', label: '数据分析' },
        { value: 'workplace_efficiency', label: '职场效率' },
        { value: 'fun_challenges', label: '趣味挑战' },
        { value: 'marketing_copy', label: '营销文案' },
        // ...其他选项
        { value: 'other', label: '其他' }
      ],
      robots: [
      ],
      is_current: true,
      dialogVisible: false,
      dataForm: {
        name: '',
        type: '',
        prompt:'',
        content:'',
      },
      newRobot:{
        id: '',
        name:'',
        type:'',
        prompt:'',
        content:'',

      }
    };
  },
  watch: {
    // 监听 selectedOption 和 customPrompt 的变化，以更新 dataForm.prompt
    selectedOption(newVal) {
      this.prompt = newVal; // 触发计算属性更新
    },
    customPrompt(newVal) {
      this.prompt = newVal; // 触发计算属性更新
    }
  },
  created(){
    this.load_models();
  },
  methods: {
    async load_models(){
      try {
        // alert("START")
        // alert(this.getSharedData)
        const response = await axios.post('http://127.0.0.1:8080/admin_sys/get_models_by_user', {
          user_id: this.$route.params.user_id,
        });
        const current_info = await axios.post('http://127.0.0.1:8080/user_sys/acquire_current_user',
          {}
        );

        this.is_current = (+ this.$route.params.user_id === +current_info.data.user_id);
        // alert(response.status);
        if (response.status === 200) {

          // alert(JSON.stringify(response.data))
          this.robots=response.data

          // 跳转到其他页面或刷新
          // window.location.href = '/dashboard'; // 示例跳转
        }
      } catch (error) {

        alert(error.response.data.error);
        //把数据改成旧数据
      }
    },
    showDetail(id){
      this.$router.push(`/modelview/model/${id}`).then(() => {
        window.location.reload();  // 页面跳转后刷新
      });
    },
    addRobot() {
      this.dialogVisible = true;
    },
    async submitForm() {
      try {
        // alert("START")
        // alert(this.getSharedData)
        const response = await axios.post('http://127.0.0.1:8080/admin_sys/add_model', {
          user_id: this.getSharedData,
          model_name: this.dataForm.name,
          model_type: this.dataForm.type,
          prompt: this.dataForm.prompt,
          content: this.dataForm.content,
        });
        // alert(response.status);
        if (response.status === 200) {
          // alert(JSON.stringify(response.data))
          await this.load_models();
          // 跳转到其他页面或刷新
          // window.location.href = '/dashboard'; // 示例跳转
        }
      } catch (error) {

        alert(error.response.data.error);
        //把数据改成旧数据
      }
      this.dialogVisible = false;
    },
    deleteRobot(id) {
      this.$confirm('此操作将永久删除该机器人, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          // alert("START")
          // alert(this.getSharedData)
          const response = await axios.post('http://127.0.0.1:8080/admin_sys/delete_model', {
            user_id: this.getSharedData,
            model_id: id,
          });
          // alert(response.status);
          if (response.status === 200) {
            // alert(response.data.message)
            this.dialogVisible = false;
            this.load_models();
            // 跳转到其他页面或刷新
            // window.location.href = '/dashboard'; // 示例跳转
          }
        } catch (error) {

          alert(error.response.data.error);
          //把数据改成旧数据
        }
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    }
  }
};

</script>

<style scoped>
.mybot-container {
  margin: 20px;
}

.el-button {
  margin-bottom: 10px; /* 给按钮添加一些底部间距 */
}
</style>

