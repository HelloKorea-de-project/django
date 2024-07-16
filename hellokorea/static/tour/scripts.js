document.addEventListener("DOMContentLoaded", function () {
  const districts = {
    "gangnam-gu": { name: "Gangnam-gu", info: "Information about Gangnam-gu." },
    "jongno-gu": { name: "Jongno-gu", info: "Information about Jongno-gu." },
    // 다른 구들의 정보 추가
  };

  const infoBox = document.getElementById("info-box");
  const districtName = document.getElementById("district-name");
  const districtInfo = document.getElementById("district-info");

  document.querySelectorAll("#seoul-map path").forEach(function (path) {
    path.addEventListener("mouseover", function () {
      const districtId = path.id;
      const district = districts[districtId];
      if (district) {
        districtName.textContent = district.name;
        districtInfo.textContent = district.info;
        infoBox.style.display = "block";
      }
    });
    path.addEventListener("mouseout", function () {
      infoBox.style.display = "none";
    });
  });
});
