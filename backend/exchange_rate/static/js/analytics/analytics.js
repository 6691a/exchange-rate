/**
 * Card Analytics
 */

'use strict';

(function() {
  let cardColor, headingColor, axisColor, shadeColor, borderColor, heatMap1, heatMap2, heatMap3, heatMap4;

  if (isDarkStyle) {
    cardColor = config.colors_dark.cardColor;
    headingColor = config.colors_dark.headingColor;
    axisColor = config.colors_dark.axisColor;
    borderColor = config.colors_dark.borderColor;
    shadeColor = 'dark';
    heatMap1 = '#4f51c0';
    heatMap2 = '#595cd9';
    heatMap3 = '#8789ff';
    heatMap4 = '#c3c4ff';
  } else {
    cardColor = config.colors.white;
    headingColor = config.colors.headingColor;
    axisColor = config.colors.axisColor;
    borderColor = config.colors.borderColor;
    shadeColor = '';
    heatMap1 = '#e1e2ff';
    heatMap2 = '#c3c4ff';
    heatMap3 = '#a5a7ff';
    heatMap4 = '#696cff';
  }




  // Total Balance - Line Chart
  // --------------------------------------------------------------------
  const totalBalanceChartEl = document.querySelector('#totalBalanceChart'),
    totalBalanceChartConfig = {
      series: [
        {
          data: [137, 210, 160, 275, 205, 315]
        }
      ],
      chart: {
        height: 225,
        parentHeightOffset: 0,
        parentWidthOffset: 0,
        zoom: { enabled: false },
        type: 'line',
        dropShadow: {
          enabled: false,
          top: 10,
          left: 5,
          blur: 3,
          color: config.colors.primary,
          opacity: 0.15
        },
        toolbar: {
          show: false
        }
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        width: 3,
        curve: 'smooth'
      },
      legend: {
        show: false
      },
      colors: [config.colors.primary],
      markers: {
        size: 6,
        colors: 'transparent',
        strokeColors: 'transparent',
        strokeWidth: 4,
        discrete: [
          {
            fillColor: config.colors.white,
            seriesIndex: 0,
            dataPointIndex: 5,
            strokeColor: config.colors.primary,
            strokeWidth: 8,
            size: 6,
            radius: 8,
          },
        ],
        hover: {
          size: 7
        }
      },
      grid: {
        show: false,
        padding: {
          top: -10,
          left: 0,
          right: 20,
          bottom: 10
        }
      },
      xaxis: {
        categories: ['10:00', '10:05', '10:10', '10:15', '10:20', '10:25'],
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        },
        labels: {
          show: false,
          style: {
            fontSize: '13px',
            colors: axisColor
          }
        }
      },
      yaxis: {
        labels: {
          show: false
        }
      },
      points: [
        {
          x: new Date('01 Dec 2017').getTime(),
          y: 8607.55,
          marker: {
            size: 8,
          },
          label: {
            borderColor: '#FF4560',
            text: 'Point Annotation'
          }
        }
      ]
    };
  if (typeof totalBalanceChartEl !== undefined && totalBalanceChartEl !== null) {
    const totalBalanceChart = new ApexCharts(totalBalanceChartEl, totalBalanceChartConfig);
    totalBalanceChart.render();
  }
})();