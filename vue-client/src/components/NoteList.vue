<script setup>
import { onMounted, ref } from 'vue';
import { useNotesStore } from '../stores/notes';
import { useAuthStore } from '../stores/auth';

const notesStore = useNotesStore();
const authStore = useAuthStore();

const newNote = ref({ title: '', description: '', tags: '' });
const search = ref('');
const filterCompleted = ref(null);

const fetchNotes = () => {
  const params = {};
  if (search.value) params.search = search.value;
  if (filterCompleted.value !== null) params.completed = filterCompleted.value;
  notesStore.fetchNotes(params);
};

onMounted(fetchNotes);

const handleAddNote = async () => {
  const tagsArray = newNote.value.tags.split(',').map(t => t.trim()).filter(t => t);
  const success = await notesStore.addNote({
    ...newNote.value,
    tags: tagsArray
  });
  if (success) {
    newNote.value = { title: '', description: '', tags: '' };
  }
};

const toggleComplete = (note) => {
  notesStore.updateNote(note.id, {
    ...note,
    completed: !note.completed
  });
};

const deleteNote = (id) => {
  if (confirm('Are you sure?')) {
    notesStore.deleteNote(id);
  }
};
</script>

<template>
  <div class="notes-container">
    <div class="header">
      <span>Welcome, {{ authStore.user?.username }}</span>
      <button @click="authStore.logout()" class="logout-btn">Logout</button>
    </div>

    <section class="add-note">
      <h3>Add New Note</h3>
      <form @submit.prevent="handleAddNote">
        <input v-model="newNote.title" placeholder="Title" required />
        <textarea v-model="newNote.description" placeholder="Description" required></textarea>
        <input v-model="newNote.tags" placeholder="Tags (comma separated)" />
        <button type="submit">Add Note</button>
      </form>
    </section>

    <section class="filters">
      <input v-model="search" @input="fetchNotes" placeholder="Search notes..." />
      <select v-model="filterCompleted" @change="fetchNotes">
        <option :value="null">All</option>
        <option :value="true">Completed</option>
        <option :value="false">Pending</option>
      </select>
    </section>

    <div v-if="notesStore.loading">Loading notes...</div>
    
    <table v-else class="notes-table">
      <thead>
        <tr>
          <th>Status</th>
          <th>Title</th>
          <th>Description</th>
          <th>Tags</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="note in notesStore.notes" :key="note.id" :class="{ completed: note.completed }">
          <td>
            <input type="checkbox" :checked="note.completed" @change="toggleComplete(note)" />
          </td>
          <td>{{ note.title }}</td>
          <td>{{ note.description }}</td>
          <td>
            <span v-for="tag in note.tags" :key="tag" class="tag">{{ tag }}</span>
          </td>
          <td>
            <button @click="deleteNote(note.id)" class="delete-btn">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.notes-container {
  max-width: 800px;
  margin: 20px auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.add-note {
  background: #eee;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}
.add-note form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.filters {
  margin-bottom: 15px;
  display: flex;
  gap: 10px;
}
.notes-table {
  width: 100%;
  border-collapse: collapse;
}
.notes-table th, .notes-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
.completed {
  background-color: #f0fdf4;
  text-decoration: line-through;
  color: #666;
}
.tag {
  background: #e2e8f0;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.8em;
  margin-right: 4px;
}
.logout-btn { background: #666; }
.delete-btn { background: #ef4444; }
button {
  padding: 5px 10px;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
