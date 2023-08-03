<template>
  <v-container fluid="">
      <div>
          <v-expansion-panels v-model="panel" multiple="">
            <v-expansion-panel>
              <v-expansion-panel-title>Монтажные работы</v-expansion-panel-title>
              <v-expansion-panel-text>
                <v-row>
                  <v-col v-for="mount in mounting"  cols="12" sm="6">
                    <v-text-field
                      v-model="mount.temp"
                      :hint="mount.text"
                      :label="mount.name"
                      prefix="Объём(кв.м./шт):"
                      :suffix="'Стоимость: '+ mount.price +' ₽'"
                       @input="up(mount.price, mount.id)"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-expansion-panel-text>
            </v-expansion-panel>

            <v-expansion-panel>
              <v-expansion-panel-title>Демонтажные работы</v-expansion-panel-title>
              <v-expansion-panel-text>
                <v-row>
                  <v-col v-for="dismant in dismantling"  cols="12" sm="6">
                    <v-text-field
                      v-model="dismant.temp"
                      :hint="dismant.text"
                      :label="dismant.name"
                      prefix="Объём(кв.м./шт):"
                      :suffix="'Стоимость: '+ dismant.price +' ₽'"
                       @input="up(dismant.price, dismant.id)"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-expansion-panel-text>
            </v-expansion-panel>

            <v-expansion-panel>
              <v-expansion-panel-title>Дополнительные работы</v-expansion-panel-title>
              <v-expansion-panel-text>
                <v-row>
                  <v-col v-for="add in additional"  cols="12" sm="6">
                    <v-text-field
                      v-model="add.temp"
                      :hint="add.text"
                      :label="add.name"
                      prefix="Объём(кв.м./шт):"
                      :suffix="'Стоимость: '+ add.price +' ₽'"
                       @input="up(add.price, add.id)"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
  </v-container>
</template>

<script>
  export default {
    name: "AdditionalWorks",
    props: {
      mounting: [],
      dismantling: [],
      additional: [],
    },
    data() {
      return {
        finalprice: 0,
        panel: [0, 1],
        selectM: [],
        selectD: [],
        selectA: [],
      }
    },
    watch:{
    },
    methods:{
      up (val, price){
        this.finalprice = this.finalprice + (price * val)
        this.$emit('additionalPricesCalculate', this.finalprice)
      },
    },
  }
</script>

<style scoped>

</style>
