import { useState, useEffect } from "react";

const useFetch = (url) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const abortConst = new AbortController();

    setTimeout(() => {
      fetch(url, { signal: abortConst.signal })
        .then((res) => {
          if (!res.ok) {
            throw Error("Could not fetch the data from resource");
          }
          return res.json();
        })
        .then((data) => {
          setData(data);
        })
        .catch((err) => {
          if (err.name === "AbortError") {
            console.log("fetch aborted");
          } else {
            console.log(err);
          }
        });
    }, 0);
    return () => abortConst.abort();
  }, [url]);

  return data;
};

export default useFetch;
