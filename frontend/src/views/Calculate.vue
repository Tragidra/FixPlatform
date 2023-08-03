<template>
  <v-container class="Calculate">
    <v-row class="packages-container" justify="center" align="stretch">
      <v-col v-for="packet in packets">
        <package-card  :packets=packet @choosePacket="choosePacket"></package-card>
      </v-col>
    </v-row>
    <v-form>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
              >
                <v-text-field
                  v-model="square"
                  hint="Введите число с точностью до одной цифры после запятой"
                  label="Общая площадь квартиры"
                  @input="up(square)"
                ></v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
              >
                <v-text-field
                  v-model="rooms"
                  hint="Введите точное целое число"
                  label="Количество комнат"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
    </v-form>
    <additional-works @additionalPricesCalculate="additionalPricesCalculate" :mounting="mounting" :dismantling="dismantling" :additional="additional">
    </additional-works>
    <v-card
      color="#23FF94"
      theme="white"
      class="mx-auto"
      max-width="370"
    >
      <v-card-item>
            <v-card-text class="text-h6 py-2">
              Итоговая стоимость: {{finalprice}} ₽
            </v-card-text>
      </v-card-item>
    </v-card>
  </v-container>
   <div class="text-center">
    <v-btn color="orange" :loading="loading" @click="saveData">
      Сохранить расчёты
      <template v-slot:loader>
        <v-progress-linear indeterminate=""></v-progress-linear>
      </template>
    </v-btn>
  </div>
</template>

<script>
import Cookies from 'js-cookie'
import PackageCard from "../components/PackageCard.vue";
import AdditionalWorks from "../components/AdditionalWorks.vue";

export default{
  name: 'Calculate',
  components: {PackageCard, AdditionalWorks},
  data() {
    return {
      square: 0,
      rooms: 0,
      choosePacketPrice: 1,
      additionalPrices: 0,
      finalprice: 0,
      loading: false,
      packets: [
        {
          'name': null,
          'price': 0,
          'text': null,
        }
      ],
      dismantling: [],
      mounting: [],
      additional: [],
      // config: {  headers: { 'X-CSRFToken': Cookies.get('csrftoken') } },
      // на будущее для интеграции с сервером
      numberRules: [
        v => !!v || 'Это поле обязательно надо заполнить!',
      ],
    }
  },
  watch: {
    loading(val) {
        if (!val) return

        setTimeout(() => (this.loading = false), 2000)
      },
  },
  created() {
    this.getPackets()
    this.getWorks()
  },
  mounted() {
  },
  methods: {
    additionalPricesCalculate: function (val){
      this.finalprice = this.finalprice + val;
    },
    choosePacket: function (val){
      console.log('1')
      this.choosePacketPrice = val;
    },
    getPackets: function (){
      this.axios.get('api/repair_packets', {}).then(response => {
              this.packets = response.data.data; })
                .catch(error => {
                  console.log(error)
                })
    },

    getWorks: function (){
      this.axios.post('api/check_fields', {mode:1}, {}).then(response => {
              this.dismantling = response.data.dismantling;
              this.mounting = response.data.mounting;
              this.additional = response.data.additional;
      })
                .catch(error => {
                  console.log(error)
                })
    },

    saveData: function (val){
      this.loading = true
    },

    up (val){
        this.finalprice = this.finalprice + (this.choosePacketPrice * val)
    },
  },
}
</script>

<style lang="scss">
</style>
