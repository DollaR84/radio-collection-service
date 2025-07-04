export default function DonatePage() {
  const cardData = [
    { currency: "€", number: "4441 1144 9720 3321" },
    { currency: "$", number: "4441 1144 8905 4781" },
    { currency: "₴", number: "4149 4993 7736 2866" },
  ];

  const paypalLink =
    "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=B3VG4L8B7CV3Y&source=url";

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      alert("Copied to clipboard");
    } catch {
      alert("Failed to copy");
    }
  };

  return (
    <div className="max-w-xl mx-auto px-4 py-10 text-center">
      <h1 className="text-3xl font-bold mb-6">Donate to the project</h1>
      <p className="mb-6 text-gray-700">
        You can support Radio Collection by transferring to a card or via PayPal.
      </p>

      <div className="space-y-4 mb-8">
        {cardData.map((card) => (
          <div
            key={card.currency}
            className="flex items-center justify-between border rounded-xl p-3 bg-gray-100"
          >
            <span className="font-medium">
              {card.currency}: {card.number}
            </span>
            <button
              onClick={() => copyToClipboard(card.number)}
              className="border px-3 py-1 rounded text-sm bg-white hover:bg-gray-200 transition"
            >
              Copy
            </button>
          </div>
        ))}
      </div>

      <div className="mt-6">
        <div className="font-medium mb-2">PayPal:</div>
        <a
          href={paypalLink}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 underline break-all"
        >
          {paypalLink}
        </a>
      </div>
    </div>
  );
}
