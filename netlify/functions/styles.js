exports.handler = async function (event, context) {
  return {
    statusCode: 200,
    body: JSON.stringify({
      styles: [
        { value: "comprehensive", name: "Comprehensive" },
        { value: "summary", name: "Summary" },
        { value: "detailed", name: "Detailed" },
        { value: "bullet_points", name: "Bullet Points" },
      ],
    }),
  };
};
