<template>
  <section id="team" class="team section-bg">
    <div class="container">
      <!-- Section Title -->
      <!--      <div class="section-title text-center">-->
      <!--        <h2>核心数据展示</h2>-->
      <!--        <p>探索我们的统计数据和分析结果</p>-->
      <!--      </div>-->

      <!-- Counts Section -->
      <section class="counts section-bg">
        <div class="container">
          <div class="row">
            <div
                v-for="(item, index) in counts"
                :key="index"
                class="col-lg-3 col-md-6 text-center count-item"
                :data-aos="'fade-up'"
                :data-aos-delay="index * 200"
            >
              <a :href="item.link">
                <div class="count-box">
                  <!-- Image icon -->
                  <img :src="item.icon" alt="Icon" class="count-icon"/>
                  <span>{{ item.count }}</span>
                  <p>{{ item.label }}</p>
                </div>
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  </section>
</template>

<script>
import botIcon from '@/img/chatbotIcon.png'
import userIcon from '@/img/userIcon.png'
import searchIcon from "@/img/searchIcon.png";
import forumIcon from "@/img/forumIcon.png"

export default {
  name: 'MainSection',
  data() {
    return {
      counts: [
        {link: '/chatbot/session/:sessionId', icon: botIcon, color: '#20b38e', label: 'Chat-Bot'},
        {link: '/user/userId/:user_id', icon: userIcon, color: '#c042ff', label: 'User Main'},
        {link: '/forum', icon: forumIcon, color: '#ffb459', label: 'Community Forum'},
        {link: '/search', icon: searchIcon, color: '#46d1ff', label: 'Search for Bot or User'}
      ]
    };
  }
}
</script>

<style scoped>
/* Scoped styles for MainSection */
.count-box {
  background-color: #fff;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 10px 10px 10px rgba(0, 0, 0, 0.1);
  text-align: center; /* Center the text inside each count box */
  border: 2px solid #ddd;  /* 设置边框为2px，颜色为灰色 */
}

.count-box img {
  width: 50px; /* Adjust the icon size */
  height: 50px;
  margin-bottom: 20px;
  object-fit: contain; /* Ensure the image keeps its aspect ratio */
}

.count-item {
  margin-bottom: 30px;
}


@media (min-width: 768px) {
  /* 2 items per row on medium screens */
  .count-item {
    flex: 1 1 48%; /* Two items in a row, taking almost equal space */
  }
}

@media (min-width: 1200px) {
  /* 4 items per row on large screens */
  .row {
    display: flex;
    flex-wrap: wrap;
  }

  .count-item {
    flex: 1 1 22%; /* Four items per row */
    margin-bottom: 20px;  /* 可选的：设置底部间隔 */
    margin-top: 20px;
  }
}

.counts .row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;  /* 设置每个box之间的间隔 */
}
</style>
