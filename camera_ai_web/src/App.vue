<template>
  <v-container :style="{ width: '600px' }">
    <v-row align="center" no-gutters style="height: 150px;">
      <v-btn color="info" v-on:click="submitFile()">Отправить файл</v-btn>
      <v-file-input @change="handleFileChange" label="Выбрать файл mp4"></v-file-input>
      <v-progress-circular v-show="isLoading" indeterminate class="ma-6"></v-progress-circular>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import Vuetify from 'vuetify'

export default {
  name: 'App',
  components: {

  },
  data: () => ({
    file: null,
    isLoading: false,
  }),
  methods: {
    handleFileChange (e) {
      console.log('handleFileChange');
      // Whenever the file changes, emit the 'input' event with the file data.
      // this.$emit('input', e.target.files[0])
      this.file = e.target.files[0];
    },
    submitFile () {
      this.isLoading = true
      let formData = new FormData();
      formData.append('file', this.file);

      axios.post('http://94.198.217.9:8000/uploadfile',
        formData,
        {
          responseType: 'blob',
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      ).then((response) => {
        this.isLoading = false
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `result.avi`);
        document.body.appendChild(link);
        link.click();
      })
        .catch((error) => {
          this.isLoading = false
          alert(error.message);
        });
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
