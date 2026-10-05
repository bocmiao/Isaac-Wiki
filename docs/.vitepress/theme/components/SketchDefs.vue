<template>
  <!-- 全站共用的手绘抖动滤镜：卡片、纸张的描边用它画出原版那种手画线条 -->
  <svg class="sketch-defs" width="0" height="0" aria-hidden="true" focusable="false">
    <filter id="ib-rough" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="4" xChannelSelector="R" yChannelSelector="G" />
    </filter>
    <filter id="ib-rough-strong" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="3" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="7" xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </svg>
</template>

<style scoped>
.sketch-defs {
  position: absolute;
  width: 0;
  height: 0;
  overflow: hidden;
}
</style>
