<template>
  <v-checkbox :label="option" :value="isSelected" @input="updateSelection" />
</template>

<script>
export default {
  props: {
    option: String,
    selectedOptions: Array,
  },
  computed: {
    isSelected() {
      return this.selectedOptions.includes(this.option);
    },
  },
  methods: {
    updateSelection(event) {
      if (event) {
        this.$emit('update', [...this.selectedOptions, this.option]);
      } else {
        this.$emit(
            'update',
            this.selectedOptions.filter((item) => item !== this.option)
        );
      }
    },
  },
};
</script>
