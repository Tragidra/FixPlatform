<template>
  <v-container fluid="">
        <v-form>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
              >
                <v-text-field
                  hint="Введите число с точностью до одной цифры после запятой"
                  model-value=""
                  label="Общая площадь квартиры"
                ></v-text-field>
            </v-col>
            <v-col
                cols="12"
                sm="6"
            >
                <v-text-field
                  hint="Введите точное целое число"
                  model-value=""
                  label="Количество комнат"
                ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>

      <v-col cols="12">
        <v-combobox
          v-model="selectM"
          :items="mounting"
          label=""
          multiple=""
          chips=""
          hint="Вы можете выбрать несколько монтажных работ из списка"
        ></v-combobox>
      </v-col>
      <v-col cols="12">
        <v-combobox
          v-model="selectD"
          :items="dismantling"
          label=""
          multiple=""
          chips=""
          hint="Вы можете выбрать несколько демонтажных работ из списка"
        ></v-combobox>
      </v-col>
      <v-col cols="12">
        <v-combobox
          v-model="selectA"
          :items="additional"
          label=""
          multiple=""
          chips=""
          hint="Вы можете выбрать несколько дополнительных работ из списка"
        ></v-combobox>
      </v-col>
  </v-container>
</template>

<script>
  export default {
    data() {
      return {
        selectM: [],
        selectD: [],
        selectA: [],
        mounting: [],
        dismantling: [],
        additional: [],
        numberRules: [
        v => !!v || 'Это поле обязательно надо заполнить!',
      ],
      }
    },
  }
</script>

<style scoped>

</style>
