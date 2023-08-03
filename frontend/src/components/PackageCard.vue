<template>
  <v-hover
      v-slot="{ isHovering, props }"
      open-delay="200"
  >
    <v-card
        :class="{ 'on-hover': isHovering }"
        :elevation="isHovering ? 16 : 2"
        v-bind="props"
        :color="packets.path"
        theme="dark"
        class="mx-auto"
        max-width="240"
        min-height="330"
    >
      <v-card-text>
        <div>Пакет услуг</div>
        <p class="text-h4 text--primary">
          {{packets.name}}
        </p>
      </v-card-text>
      <v-card-text>
        <p class="text-h6 text-decoration-underline">
          {{packets.price}} руб/кв.м</p>
      </v-card-text>
      <v-card-text>
        <div class="font-italic">
          Качественный ремонт с использованием самых лучшимх материалов, большой выбор и уникальные дизайнерские проекты<br>
        </div>
      </v-card-text>
      <v-card-actions class="pt-0">
        <v-btn
            variant="text"
            color="#00FA9A"
            @click="reveal = true"
        >
          Узнать подробнее
        </v-btn>
        </v-card-actions>
         <v-card-actions class="pt-0">
        <v-btn
            variant="text"
            color="#00FFFF"
            @click="selectPacket(packets.price)"
        >
          Выбрать
        </v-btn>
      </v-card-actions>

      <v-expand-transition>
        <v-card
            v-if="reveal"
            class="v-card--reveal"
            style="height: 100%;"
        >
          <v-card-text class="pb-0">
            <p class="text-h4 text--primary">
              Набор услуг
            </p>
            <p>{{packets.text}}</p>
          </v-card-text>
          <v-card-actions class="pt-0">
            <v-btn
                variant="text"
                color="red"
                @click="reveal = false"
            >
              Закрыть
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-expand-transition>
    </v-card>
  </v-hover>
</template>

<script>
export default {
  name: "PackageCard",
  props: {
    packets: [],
  },
  data: () => ({
    reveal: false,
  }),
  methods: {
    selectPacket: function (packet){
      this.$emit('choosePacket', packet)
    }
  },
}
</script>
<style>

.v-card--reveal {
  bottom: 0;
  opacity: 1 !important;
  position: absolute;
  width: 100%;
}
</style>
<style lang="sass">
.v-card.on-hover.v-theme--light
    background-color: rgba(#C371FFFF, 1)
    >.v-card__text
      color: #c371ff
</style>
