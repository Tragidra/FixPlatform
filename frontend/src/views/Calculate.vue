<template>
  <v-container class="Calculate">
    <v-row class="packages-container" justify="center" align="stretch">
      <v-col v-for="packet in packets">
        <package-card  :packets=packet ></package-card>
      </v-col>
    </v-row>
    <additional-option>
    </additional-option>
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
import AdditionalOption from "../components/AdditionalOption.vue";

export default{
  name: 'Calculate',
  components: {PackageCard, AdditionalOption},
  data() {
    return {
      loading: false,
      packets: [
        {
          'name': null,
          'price': 0,
          'text': null,
        }
      ],
      // config: {  headers: { 'X-CSRFToken': Cookies.get('csrftoken') } },
      // на будущее для интеграции с сервером
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
  },
  mounted() {
  },
  methods: {
    getPackets: function (){
      this.axios.get('api/repair_packets', {}).then(response => {
              this.packets = response.data.data; })
                .catch(error => {
                  console.log(error)
                })
    },
    saveData: function (val){
      this.loading = true
    },

  },
}
</script>

<style lang="scss">
</style>
