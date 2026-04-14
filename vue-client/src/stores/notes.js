import { defineStore } from 'pinia';
import Api from '../Api';

export const useNotesStore = defineStore('notes', {
  state: () => ({
    notes: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchNotes(params = {}) {
      this.loading = true;
      try {
        const response = await Api.getNotes(params);
        this.notes = response.data;
      } catch (err) {
        this.error = 'Failed to fetch notes';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async addNote(note) {
      try {
        const response = await Api.createNote(note);
        this.notes.unshift(response.data);
        return true;
      } catch (err) {
        this.error = 'Failed to add note';
        return false;
      }
    },
    async updateNote(id, noteData) {
      try {
        const response = await Api.updateNote(id, noteData);
        const index = this.notes.findIndex(n => n.id === id);
        if (index !== -1) {
          this.notes[index] = response.data;
        }
        return true;
      } catch (err) {
        this.error = 'Failed to update note';
        return false;
      }
    },
    async deleteNote(id) {
      try {
        await Api.deleteNote(id);
        this.notes = this.notes.filter(n => n.id !== id);
        return true;
      } catch (err) {
        this.error = 'Failed to delete note';
        return false;
      }
    }
  },
});
