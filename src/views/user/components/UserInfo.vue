<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>个人信息</span>
      <el-button style="float: right;" type="primary" @click="toggleEdit" v-if="is_current">编辑</el-button>
      <el-button style="float: right;margin-right: 10px;" type="primary" @click="openRecharge" v-if="is_current">充值</el-button>
    </div>
    <div v-if="!editMode" class="text item">
      <!-- 非编辑模式下的只读信息展示 -->
      <el-form label-width="80px">
        <el-form-item label="头像">
          <img v-if="userInfo.image" :src="userInfo.image" class="avatar" />
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-form-item>
        <el-form-item label="UID">{{ userInfo.user_id }}</el-form-item>
        <el-form-item label="用户名">{{ userInfo.username }}</el-form-item>
        <el-form-item label="性别">{{ userInfo.gender }}</el-form-item>
        <el-form-item label="生日">{{ userInfo.birthday }}</el-form-item>
        <el-form-item label="积分" v-if="is_current">{{ userInfo.score }}</el-form-item>
      </el-form>
    </div>
    <div v-if="editMode" class="text item">
      <!-- 编辑模式下的表单 -->
      <el-form ref="dataForm" :model="userInfo" label-width="80px">
        <el-form-item label="头像">
          <el-upload
              class="avatar-uploader"
              action="https://jsonplaceholder.typicode.com/posts/"
              :show-file-list="false"
              :on-success="handleAvatarSuccess"
              :before-upload="beforeAvatarUpload"
          >
            <img v-if="userInfo.image" :src="userInfo.image" class="avatar" />
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </el-form-item>
<!--        <el-form-item label="用户名">-->
<!--        <el-input v-model="userInfo.username" />-->
<!--        </el-form-item>-->
        <el-form-item label="性别">
          <el-input v-model="userInfo.gender" />
        </el-form-item>
        <el-form-item label="生日">
          <el-input v-model="userInfo.birthday" />
        </el-form-item>
<!--        <el-form-item label="积分">-->
<!--          <el-input type="textarea" v-model="userInfo.score" />-->
<!--        </el-form-item>-->
        <el-form-item label="旧密码">
          <el-input type="textarea" v-model="userInfo.old_password" />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input type="textarea" v-model="userInfo.new_password" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">更新信息</el-button>
          <el-button @click="toggleEdit">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-card>

  <!-- 编辑模式下的弹出窗口 -->
  <el-dialog v-model="dialogVisible" title="充值">
    <el-form :model="userInfo" label-width="80px">
      <el-form-item label="输入充值金额" prop="increament">
        <el-input
          type="textarea"
          v-model.number="userInfo.increament"
          @input="handleInput"
          autocomplete="off"
          maxlength="9"
        />
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="submitRecharge">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>
import axios from "axios";
import {mapActions, mapGetters} from 'vuex';
export default {
  computed: {
    ...mapGetters(['getSharedData']),
  },
  name: 'UserInfo',
  data() {
    return {
      is_current: true,
      editMode: false,
      dialogVisible: false,
      rules: {
        increament: [
          { required: true, message: '请输入充值金额', trigger: 'blur' },
          { pattern: /^[1-9]\d*$/, message: '请输入一个正整数', trigger: 'blur' }
        ]
      },
      userInfo: {
        user_id:'1',
        username: '',
        gender: 'male',
        birthday: '2004-1-1',
        score: '50',
        image: 'https://multiavatar.com/img/logo-animated.gif?v=003', // 用户头像的URL
        password:'123456',
        old_password:'',
        new_password:'',
        increament:'',

      }
    };
  },
  created() {
    this.userInfo.user_id = this.$route.params.user_id
    this.getUserData();
  },
  methods: {
    handleInput(value) {
      // 移除非数字字符
      this.userInfo.increament = value.replace(/\D/g, '');
    },
    toggleEdit() {
      this.editMode = !this.editMode;
    },
    openRecharge(){
      this.dialogVisible = true;
    },
    async getUserData() {
      const new_info = await axios.post('http://127.0.0.1:8080/user_sys/user',
          {user_id: this.userInfo.user_id}
      );
      const current_info = await axios.post('http://127.0.0.1:8080/user_sys/acquire_current_user',
          {}
      );
      this.is_current = (+this.userInfo.user_id === +current_info.data.user_id);
      // alert(JSON.stringify(new_info.data))
      this.userInfo.username = new_info.data.username;
      this.userInfo.gender = new_info.data.gender;
      this.userInfo.birthday = new_info.data.birthday;
      this.userInfo.image = new_info.data.image;
      this.userInfo.score = new_info.data.score;
      // alert(this.userInfo.user_id);
      this.$store.commit('updateSharedData', {
        userid: this.userInfo.user_id
      });
      // alert(this.getSharedData)
      // alert(JSON.stringify(this.userInfo))
    },
    async submitForm() {
      this.$message('提交表单');
      try {

        const response = await axios.post('http://127.0.0.1:8080/user_sys/update', this.userInfo);
        // alert(response.status);
        if (response.status === 200) {
          alert(response.data.message); // 显示成功消息
          const new_info = await axios.post('http://127.0.0.1:8080/user_sys/user',
            this.userInfo
          );
          // alert(JSON.stringify(new_info.data));
          this.userInfo.user_id = new_info.data.user_id;
          this.userInfo.name = new_info.data.username;
          this.userInfo.gender = new_info.data.gender;
          this.userInfo.birthday = new_info.data.birthday;
          this.userInfo.image = new_info.data.image;
          this.userInfo.score = new_info.data.score;
          // 跳转到其他页面或刷新
          // window.location.href = '/dashboard'; // 示例跳转
        }
        else {
          alert("Unknown Error!")
        }
      } catch (error) {

          // 后端返回的错误消息
          // errorMessage.value = error.response.data.message;
          alert(error.response.data.message);
          //把数据改成旧数据
      }
      this.editMode = !this.editMode;
    },
    async submitRecharge() {
      this.$message('提交表单');
      try {
        const response = await axios.post('http://127.0.0.1:8080/store_sys/update',
            this.userInfo
        );
        if (response.status === 200) {
          alert(response.data.message); // 显示成功消息
          const new_info = await axios.post('http://127.0.0.1:8080/user_sys/user',
            this.userInfo
          );
          // alert(JSON.stringify(new_info.data))
          this.userInfo.name = new_info.data.username;
          this.userInfo.gender = new_info.data.gender;
          this.userInfo.birthday = new_info.data.birthday;
          this.userInfo.image = new_info.data.image;
          this.userInfo.score = new_info.data.score;
          // 跳转到其他页面或刷新
          // window.location.href = '/dashboard'; // 示例跳转
        }
      } catch (error) {

          // 后端返回的错误消息
          // errorMessage.value = error.response.data.message;
          alert(error.response.data.message);
          //把数据改成旧数据
      }
      this.dialogVisible = false;
    },
    handleAvatarSuccess(response, file, fileList) {
      this.userInfo.image = URL.createObjectURL(file.raw);
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!');
      }
      return isJPG && isLt2M;
    }
  }
};
</script>

<style scoped>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: '';
}

.clearfix:after {
  clear: both;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 80px;
  height: 80px;
  line-height: 80px;
  text-align: center;
}

.avatar {
  width: 80px;
  height: 80px;
  display: block;
}
</style>