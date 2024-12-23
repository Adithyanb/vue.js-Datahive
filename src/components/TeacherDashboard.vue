/* eslint-disable no-unused-vars */
<template>
  <div class="teacher-dashboard">
    <div class="header">
      <h1 class="app-title">DataHive</h1>
    </div>
    <div class="content">
      <div class="left-section">
        <h2>File Upload</h2>
        <div class="file-upload">
          <input type="file" @change="handleFileSelection" />
          <input type="text" v-model="textToUpload" placeholder="Enter text to upload" />
          <button @click="uploadFileAndText">Upload</button>
        </div>
        <div class="uploaded-items">
          <h3>Uploaded Items</h3>
          <div v-for="item in uploadedItems" :key="item.id" class="uploaded-item">
            <div>{{ item.fileName }} ({{ item.fileType }})</div>
            <div>Uploaded at: {{ item.uploadedAt }}</div>
            <button @click="deleteItem(item.id)">Delete</button>
          </div>
        </div>
      </div>
      <div class="right-section">
        <div class="interaction-result-box">
          <h3>Retrieved Answer</h3>
          <div class="retrieved-answer">{{ interactionResult }}</div>
        </div>
        <div class="text-interaction">
          <input type="text" v-model="textToInteract" placeholder="Enter text to interact" />
          <button @click="interactWithText">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TeacherDashboard',
  data() {
    return {
      username: 'manas',
      textToUpload: '',
      selectedFile: null,
      uploadedItems: [],
      textToInteract: '',
      interactionResult: ''
    };
  },
  mounted() {
    
    this.fetchUploadedItems();
  },
  methods: {
    handleFileSelection(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFileAndText() {
      try {
        const formData = new FormData();
        
        
        if (this.selectedFile) {
          formData.append('file', this.selectedFile);
        }
        
        
        if (this.textToUpload) {
          formData.append('text', this.textToUpload);
        }

        await axios.post('http://localhost:5000/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        
        await this.fetchUploadedItems();

        
        this.textToUpload = '';
        this.$el.querySelector('input[type="file"]').value = '';
        this.selectedFile = null;
      } catch (error) {
        console.error('Upload failed:', error);
        alert('Upload failed');
      }
    },
    async fetchUploadedItems() {
      try {
        const response = await axios.get('http://localhost:5000/api/uploaded-items');
        this.uploadedItems = response.data;
      } catch (error) {
        console.error('Failed to fetch uploaded items:', error);
      }
    },
    async deleteItem(id) {
      try {
        await axios.delete(`http://localhost:5000/api/delete-item/${id}`);
        
        await this.fetchUploadedItems();
      } catch (error) {
        console.error('Delete failed:', error);
        alert('Delete failed');
      }
    },
    async interactWithText() {
      try {
        const response = await axios.post('http://localhost:5000/api/interact', {
          text: this.textToInteract
        });

        this.interactionResult = response.data.result;
        this.textToInteract = '';
      } catch (error) {
        console.error('Interaction failed:', error);
        this.interactionResult = 'Interaction failed';
      }
    }
  }
};
</script>



<style scoped>
.teacher-dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
  background-color: #121212;
  color: #ffffff;
}

.header {
  text-align: center;
  padding: 20px 0;
  background-color: #1f1f1f;
}

.app-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #ffffff;
}

.content {
  display: flex;
  gap: 20px;
}

.left-section {
  flex: 0.4;
  padding: 20px;
  background-color: #1e1e1e;
  border: 1px solid #333;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-section {
  flex: 0.6;
  padding: 20px;
  background-color: #1e1e1e;
  border: 1px solid #333;
  border-radius: 8px;
}

.file-upload {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-upload input[type="file"] {
  background-color: #2c2c2c;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  padding: 5px;
}

.file-upload input[type="text"] {
  background-color: #2c2c2c;
  color: #ffffff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 5px;
}

.file-upload button {
  background-color: #3a3a3a;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
}

.uploaded-items .uploaded-item {
  margin: 10px 0;
  background-color: #2c2c2c;
  padding: 10px;
  border-radius: 4px;
}

.text-interaction {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.text-interaction input[type="text"] {
  background-color: #2c2c2c;
  color: #ffffff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 5px;
}

.text-interaction button {
  background-color: #3a3a3a;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
}

.interaction-result {
  background-color: #2c2c2c;
  color: #ffffff;
  padding: 20px;
  border-radius: 4px;
  font-size: 1.2rem;
  height: 200px;
  overflow-y: auto;
}

.interaction-result-box {
  margin-bottom: 20px;
  background-color: #2c2c2c;
  padding: 10px;
  border-radius: 4px;
}

.retrieved-answer {
  background-color: #1e1e1e;
  color: #ffffff;
  padding: 20px;
  border-radius: 4px;
  font-size: 1.2rem;
  min-height: 200px;
}
</style>
