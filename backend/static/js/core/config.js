/**
 * Config
 * -------------------------------------------------------------------------------------
 * ! IMPORTANT: Make sure you clear the browser local storage In order to see the config changes in the template.
 * ! To clear local storage: (https://www.leadshook.com/help/how-to-clear-local-storage-in-google-chrome-browser/).
 */

'use strict';

// JS global variables
let config = {
  colors: {
    primary: '#696cff',
    secondary: '#8592a3',
    success: '#71dd37',
    info: '#03c3ec',
    warning: '#ffab00',
    danger: '#ff3e1d',
    dark: '#233446',
    black: '#000',
    white: '#fff',
    body: '#f4f5fb',
    headingColor: '#566a7f',
    axisColor: '#a1acb8',
    borderColor: '#eceef1'
  },
  colors_label: {
    primary: '#666ee81a',
    secondary: '#8897aa1a',
    success: '#28d0941a',
    info: '#1e9ff21a',
    warning: '#ff91491a',
    danger: '#ff49611a',
    dark: '#181c211a'
  },
  colors_dark: {
    cardColor: '#2b2c40',
    headingColor: '#cbcbe2',
    axisColor: '#7071a4',
    borderColor: '#444564'
  },
  enableMenuLocalStorage: true // Enable menu state with local storage support
};

let assetsPath = document.documentElement.getAttribute('data-assets-path'),
  templateName = document.documentElement.getAttribute('data-template'),
  mode = document.documentElement.getAttribute('data-mode'),
  debug = document.documentElement.getAttribute('data-debug'),
  rtlSupport = true; // set true for rtl support (rtl + ltr), false for ltr only.
/**
* TemplateCustomizer
* ! You must use(include) template-customizer.js to use TemplateCustomizer settings
* -----------------------------------------------------------------------------------------------
*/

// To use more themes, just push it to THEMES object.

/* TemplateCustomizer.THEMES.push({
  name: 'theme-raspberry',
  title: 'Raspberry'
}); */

// To add more languages, just push it to LANGUAGES object.
/*
TemplateCustomizer.LANGUAGES.fr = { ... };
*/

/**
 * TemplateCustomizer settings
 * -------------------------------------------------------------------------------------
 * cssPath: Core CSS file path
 * themesPath: Theme CSS file path
 * displayCustomizer: true(Show customizer), false(Hide customizer)
 * lang: To set default language, Add more langues and set default. Fallback language is 'en'
 * controls: [ 'rtl','style','layoutType','showDropdownOnHover','layoutNavbarFixed','layoutFooterFixed','themes'] | Show/Hide customizer controls
 * defaultTheme: 0(Default), 1(Semi Dark), 2(Bordered)
 * defaultStyle: 'light', 'dark' (Mode)
 * defaultTextDir: 'ltr', 'rtl' (rtlSupport must be true for rtl mode)
 * defaultLayoutType: 'static', 'fixed'
 * defaultMenuCollapsed: true, false
 * defaultNavbarFixed: true, false
 * defaultFooterFixed: true, false
 * defaultShowDropdownOnHover : true, false (for horizontal layout only)
 */

const host = debug ? 'http://127.0.0.1:8000' : window.location.protocol + '//' + window.location.hostname
const path = '/api/v1/'
const api_path = host + path
const static_host = debug ? host + '/' : 'https://s3-exchange-rate.s3.ap-northeast-2.amazonaws.com/'

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const http = axios.create({
  baseURL: api_path,
  headers: {
    "X-CSRFToken": `${getCookie('csrftoken')}`,
  },
});
const float_digit = 2;


if (typeof TemplateCustomizer !== 'undefined') {
  window.templateCustomizer = new TemplateCustomizer({
    cssPath: static_host + assetsPath + '/css/core' + '' + '/',
    themesPath: static_host + assetsPath + '/css/core' + '' + '/',
    displayCustomizer: false,
    // lang: 'fr',
    // defaultTheme: 2,
    defaultStyle: mode,
    // defaultTextDir: 'ltr',
    // defaultLayoutType: 'fixed',
    // defaultMenuCollapsed: true,
    // defaultNavbarFixed: true,
    // defaultFooterFixed: false
    defaultShowDropdownOnHover: true,
    // controls: [
    //   'rtl',
    //   'style',
    //   'layoutType',
    //   'showDropdownOnHover',
    //   'layoutNavbarFixed',
    //   'layoutFooterFixed',
    //   'themes'
    // ],
  });
}
