window.SupportConfig = Object.freeze({
  paymentsEnabled: false,
  checkoutEndpoint: "",
  successUrl: "support-thanks.html",
  supportedCurrencies: ["NOK", "EUR", "USD"],
  suggestedAmounts: {
    NOK: [100, 250, 500, 1000, 10000],
    EUR: [10, 25, 50, 100, 1000],
    USD: [10, 25, 50, 100, 1000]
  },
  providers: {
    vipps: { enabled: false, currencies: ["NOK"] },
    stripe: { enabled: false, currencies: ["NOK", "EUR", "USD"] }
  }
});
