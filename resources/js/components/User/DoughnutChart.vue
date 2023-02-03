<template>
  <div class="">
    <pie-chart width="400px" height="300px" :data="data"></pie-chart>
  </div>
</template>

<script>
import Vue from 'vue'
import Chartkick from 'vue-chartkick'
import Chart from 'chart.js'

Vue.use(Chartkick.use(Chart))

export default {
    name: "Doughnut",
    props: {
        width: {
            type: Number,
            default: 244,
        },
        height: {
            type: Number,
            default: 244,
        },
        total: {
            type: Number,
            required: false,
        },
        title: {
            type: String,
            required: false,
            default: null,
        },
        isCurrency: {
            type: Boolean,
            default: false,
            required: false,
        },
        totalLabel: {
            type: String,
            required: false,
            default: "Total devices",
        },
        chartData: {
            type: Object,
            required: false,
            default: () => ({
                datasets: [
                    {
                        data: [48, 19, 29, 4],
                        backgroundColor: ["#016667", "#DAB75D", "#B5CBCB", "#DAE5E6"],
                    },
                ],
                labels: ["Available", "Missing", "In-use", "Repair"],
            }),
        },
        chartOptions: {
            type: Object,
            default: () => ({
                responsive: true,
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                // maintainAspectRatio: false,
                // animation: {
                //   animateRotate: false,
                // },
            }),
        },
    },

    data(){

        return{

            data: [["AUDCAD",0.030198846705080037],
                ["USDCHF",0.023309422178962702],
                ["USDJPY",0.015526875132245911],
                ["EURAUD",0.029987413669538054],
                ["EURUSD",0.01351781123507792],
                ["USDHKD",0.5080251157650817],
                ["USDT/USD",0.32069559658742075],
                ["DAI/USD",0.04742068208950436]]
        }
    },

    mounted(){





    },

    computed: {
        // datasets() {
        //     const totalSum = props.chartData.datasets[0].data.reduce((a, b) => {
        //         return a + b;
        //     }, 0);
        //     return props.chartData.datasets[0].data.map((value, i) => {
        //         return {
        //             value,
        //             percentage: `(${Math.round((value / totalSum) * 100)}%)`,
        //             color: props.chartData.datasets[0].backgroundColor[i],
        //             label: props.chartData.labels[i],
        //         };
        //     });
        // }

    },

    methods: {
    }
}



</script>
