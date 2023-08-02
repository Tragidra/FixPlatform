<template>
  <v-container class="Calculate">
    <v-row class="packages-container" justify="center" align="stretch">
      <v-col v-for="packet in packets">
        <package-card> :packets= </package-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import Cookies from 'js-cookie'
import PackageCard from "../components/PackageCard.vue";

export default{
  name: 'Calculate',
  components: {PackageCard},
  data() {
    return {
      packets: [],
      // config: {  headers: { 'X-CSRFToken': Cookies.get('csrftoken') } },
      // на будущее для интеграции с сервером
    }
  },
  watch: {
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

  },
}
</script>

<style lang="scss">
</style>
