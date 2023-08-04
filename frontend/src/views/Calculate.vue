<template>
   <v-alert
      v-model="alert"
      border="start"
      variant="tonal"
      closable=""
      type="info"
      close-label="Close Alert"
      color="deep-purple-accent-4"
      title="Добро пожаловать в калькулятор стоимости ремонта компании FIX-ремонт!"
      text="Здесь вы можете рассчитать стоимость ремонта квартиры или дома в нашей компании, опираясь на наши расценки.
      Алгоритм работы с калькулятором:
      1) Выберите один из предлагаемых пакетов услуг, нажав на кнопку 'Выбрать'. Если вы хотите узнать, что входит в состав
      пакета, то нажмите на кнопку 'Узнать подробнее'.
      2) Введите общую площадь вашей квартиры/дома и количество комнат в соответствующих полях ниже.
      3) Выберите дополнительные услуги, нажам на поля 'Монтажные работы', 'Демонтажные работы' или 'Дополнительные работы'.
      Выберите конкретные опции, введя объём работ (в кв.м. или штуках) в соответствующее поле.
      4) При каждом вашем выборе цена подсчитывается автоматически, вы можете посмотреть её промотав вниз в поле 'Итоговая стоимость'.
      5) Если вы желаете сохранить данные расчётов в файл, то после составления финального варианта нажмите на кнопку 'Сохранить расчёты'. Удачи!"
    ></v-alert>
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
                  :disabled="disable"
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
                  :disabled="disable"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
    </v-form>
    <additional-works :disable="disable" @additionalPricesCalculate="additionalPricesCalculate" :mounting="mounting" :dismantling="dismantling" :additional="additional">
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
      disable: true,
      alert: true,
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
      this.choosePacketPrice = val;
      this.alert = false
      this.disable = false
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

    clearSquare() {
        this.square = 0
      },

    clearRooms() {
        this.rooms = 0
      },
  },
}
</script>

<style lang="scss">

</style>
