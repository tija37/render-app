document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btn");
  const output = document.getElementById("output");

  let paycheck = 0;
  
  btn.addEventListener("click", async () => {
    // Get current date
    const now = new Date();

    // First day of the current month at 08:00
    const firstDay = new Date(now.getFullYear(), now.getMonth(), 1, 8, 0);
    
    // Current date and time
    const current = now;

    // Format as YYYY-MM-DDTHH:MM
    const formatDate = (d) => {
      const pad = (n) => String(n).padStart(2, "0");
      return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
    };

    const startStr = formatDate(firstDay);
    const endStr = formatDate(current);

    try {
      const res = await fetch(`/api/working_hours?start=${startStr}&end=${endStr}`);
      if (!res.ok) throw new Error("Network response was not OK");
      const data = await res.json();
      //output.innerText = `Working hours this month: ${data.working_hours}`;

      output.style.display = "block";

    // Disable button to prevent multiple clicks
      btn.disabled = true;
      paycheck = data.working_hours * 13.29;
    // Start counter
      intervalId = setInterval(() => {
        paycheck += 0.0036916;
        output.innerText = paycheck + "€";
     }, 1000);

    } catch (err) {
      output.innerText = "Error: " + err;
    }
  });

});