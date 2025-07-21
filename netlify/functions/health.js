exports.handler = async function (event, context) {
  return {
    statusCode: 200,
    body: JSON.stringify({
      status: "healthy",
      message: "YouTube Notes Generator API is running",
      version: "2.0.0",
      timestamp: new Date().toISOString(),
    }),
  };
};
