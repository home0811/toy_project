let backEndServerAddress = 'http://192.168.0.111:8000/';
// url 에서 parameter 추출

function getParam(sname) {
  let params = location.search.substr(location.search.indexOf('?') + 1);
  let sval = '';
  params = params.split('&');
  for (let i = 0; i < params.length; i++) {
    temp = params[i].split('=');
    if ([temp[0]] == sname) {
      sval = temp[1];
    }
  }
  return sval;
}

function mapCreateRequest(name) {
  let data = manager.getData();
  $.ajax({
    type: 'POST',
    data: { data },
    url: `${backEndServerAddress}api/storage/?name=${name}`,
    success: function (res) {
      location.reload();
    },
  });
}

function mapGetRequest(page, count) {
  $.ajax({
    type: 'GET',
    url: `${backEndServerAddress}api/storage/?page=${page}&count=${count}`,
    success: function (res) {
      buildMapList(res.map);
      buildMapListPagination(page, count, res.total);
    },
  });
}

function mapUpdateRequest(name) {
  let data = manager.getData();
  $.ajax({
    type: 'PUT',
    data: { data },
    url: `${backEndServerAddress}api/storage/?name=${name}&id=${updateId}`,
    success: function (res) {
      location.reload();
    },
  });
}

function mapDeleteRequest(id) {
  $.ajax({
    type: 'DELETE',
    url: `${backEndServerAddress}api/storage/?id=${id}`,
    success: function (res) {
      location.reload();
    },
  });
}

// 저장한 Map 데이터를 불러오는 함수입니다
function addMap(data) {
  // 그리기 중이면 그리기를 취소합니다
  manager.cancel();

  // 기존의 Map 객체들 삭제
  removeOverlays();

  if (data.type == 'polygon') {
    drawPolygon(data);
  } else {
    drawPolyline(data);
  }

  updateId = data.id;
  storageBtn.disabled = false;
  storageBtn.innerText = '수정하기';
  storageBtn.value = 'update';
  nameInput.disabled = false;
  nameInput.value = data.name;
}

// 페이지 로드 후 불러오기 function
window.addEventListener('DOMContentLoaded', function () {
  let page = getParam('page') == '' ? 1 : Number(getParam('page'));
  let count = getParam('count') == '' ? 20 : Number(getParam('count'));
  mapGetRequest(page, count);
});

function buildMapList(map) {
  let div = document.getElementById('map-list');

  // map-list 자식 노드가 있을 경우 전체 삭제
  if (div.hasChildNodes()) {
    while (div.hasChildNodes()) {
      div.removeChild(div.firstChild);
    }
  }

  // map-list 추가
  for (let i = 0; i < map.length; i++) {
    div.innerHTML += getRow(map[i].name, map[i].id);
  }

  for (let i = 0; i < map.length; i++) {
    addMapListEvent(map[i]);
  }
}

//
function getRow(title, id) {
  return `
   <div class="row">
      <div class="col-9">
        <div class="row"><button id="map-button-${id}-${title}" type="button" class="btn btn-primary btn-sm">${title}</button></div>
      </div>
      <div class="col-3">
      <div class="row">
        <i id="remove-button-${id}-${title}" class="bi bi-x-circle btn btn-danger btn-sm"></i>
      </div>
      </div>
    </div>`;
}

// param map
function addMapListEvent(map) {
  let mapBtn = document.getElementById(`map-button-${map.id}-${map.name}`);
  mapBtn.addEventListener('click', () => addMap(map));

  let removeBtn = document.getElementById(`remove-button-${map.id}-${map.name}`);
  removeBtn.addEventListener('click', () => mapDeleteRequest(map.id));
}

function isNext(lastPage, total) {
  return lastPage < total ? true : false;
}

function isPrev(firstPage) {
  return firstPage > 1 ? true : false;
}

function next(lastPage, count, total) {
  if (isNext(lastPage, total)) mapGetRequest(lastPage + 1, count);
}

function prev(firstPage, count) {
  if (isPrev(firstPage)) mapGetRequest(firstPage - 1, count);
}

function addPageEvent(first_page, last_page, count, total, arrPage) {
  let firstPage = document.getElementById(`first-page`);
  firstPage.addEventListener('click', () => mapGetRequest(1, count));

  let prevPage = document.getElementById(`prev-page`);
  prevPage.addEventListener('click', () => prev(first_page, count));

  for (const p in arrPage) {
    let middlePage = document.getElementById(`page-${arrPage[p]}`);
    middlePage.addEventListener('click', () => mapGetRequest(arrPage[p], count));
  }

  let nextPage = document.getElementById(`next-page`);
  nextPage.addEventListener('click', () => next(last_page, count, total));

  let lastPage = document.getElementById(`last-page`);
  lastPage.addEventListener('click', () => mapGetRequest(total, count));
}

function buildMapListPagination(page, count, total) {
  let div = document.getElementById('map-list-pagination');

  if (div.hasChildNodes()) {
    while (div.hasChildNodes()) {
      div.removeChild(div.firstChild);
    }
  }

  let viewPage = 3;
  let arrPage = [];
  let page_group = Math.ceil(page / viewPage);
  let last_page = page_group * viewPage;
  if (last_page > total) last_page = total;
  let first_page = last_page - (viewPage - 1);
  if (first_page == 0) first_page = 1;

  for (let i = first_page; i <= last_page; i++) arrPage.push(i);

  let pagination = `<nav aria-label="Page navigation example">
                      <ul class="pagination">
                        <li class="page-item">
                          <button id="first-page" class="page-link" aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                          </button>
                        </li>
                        <li class="page-item">
                          <button id="prev-page" class="page-link">
                            <span aria-hidden="true">&lsaquo;</span>
                          </button>
                        </li>`;

  for (const p in arrPage) {
    pagination += `<li class="page-item"><button id="page-${arrPage[p]}" class="page-link">${arrPage[p]}</button></li>`;
  }

  pagination += `<li class="page-item">
                  <button id="next-page" class="page-link">
                    <span aria-hidden="true">&rsaquo;</span>
                  </button>
                </li>
                <li class="page-item">
                  <button id="last-page" class="page-link" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                  </button>
                </li>
              </ul>
            </nav>`;
  div.innerHTML += pagination;

  addPageEvent(first_page, last_page, count, total, arrPage);
}

// Drawing Manager로 도형을 그릴 지도 div
let drawingMapContainer = document.getElementById('drawingMap'),
  drawingMap = {
    center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
    level: 3, // 지도의 확대 레벨
  };

// 지도를 표시할 div와  지도 옵션으로  지도를 생성합니다
drawingMap = new kakao.maps.Map(drawingMapContainer, drawingMap);

let options = {
  // Drawing Manager를 생성할 때 사용할 옵션입니다
  map: drawingMap, // Drawing Manager로 그리기 요소를 그릴 map 객체입니다
  drawingMode: [
    // Drawing Manager로 제공할 그리기 요소 모드입니다
    kakao.maps.drawing.OverlayType.POLYLINE,
    kakao.maps.drawing.OverlayType.POLYGON,
  ],
  // 사용자에게 제공할 그리기 가이드 툴팁입니다
  // 사용자에게 도형을 그릴때, 드래그할때, 수정할때 가이드 툴팁을 표시하도록 설정합니다
  guideTooltip: ['draw', 'drag', 'edit'],

  polylineOptions: {
    // 선 옵션입니다
    draggable: true, // 그린 후 드래그가 가능하도록 설정합니다
    removable: true, // 그린 후 삭제 할 수 있도록 x 버튼이 표시됩니다
    editable: true, // 그린 후 수정할 수 있도록 설정합니다
    strokeColor: '#39f', // 선 색
    hintStrokeStyle: 'dash', // 그리중 마우스를 따라다니는 보조선의 선 스타일
    hintStrokeOpacity: 0.5, // 그리중 마우스를 따라다니는 보조선의 투명도
  },

  polygonOptions: {
    draggable: true,
    removable: true,
    editable: true,
    strokeColor: '#39f',
    fillColor: '#39f',
    fillOpacity: 0.5,
    hintStrokeStyle: 'dash',
    hintStrokeOpacity: 0.5,
  },
};

// 위에 작성한 옵션으로 Drawing Manager를 생성합니다
let manager = new kakao.maps.drawing.DrawingManager(options),
  drawOverlays = [],
  updateId = '';

// 저장하기 버튼
let storageBtn = document.getElementById('storage');

// 이름 입력 박스
let nameInput = document.getElementById('map-name');

// 지도에 그려진 도형이 있다면 모두 지웁니다
function removeOverlays() {
  // 추가된 도형 삭제
  let data = manager.getOverlays();
  let polygonLen = data.polygon.length,
    polylineLen = data.polyline.length,
    i = 0,
    j = 0;

  for (; i < polygonLen; i++) {
    data.polygon[i].remove();
  }

  for (; j < polylineLen; j++) {
    data.polyline[j].remove();
  }

  // 그려진 도형 삭제
  let len = drawOverlays.length;
  i = 0;

  for (; i < len; i++) {
    manager.remove(drawOverlays[i]);
  }

  drawOverlays = [];
}

// 버튼 클릭 시 호출되는 핸들러 입니다
function selectOverlay(type) {
  removeOverlays();

  // 그리기 중이면 그리기를 취소합니다
  manager.cancel();

  // 클릭한 그리기 요소 타입을 선택합니다
  manager.select(kakao.maps.drawing.OverlayType[type]);
}

// 그리기가 끝날 때 저장하기 버튼을 활성화합니다
manager.addListener('drawend', function (data) {
  storageBtn.disabled = false;
  nameInput.disabled = false;

  drawOverlays.push(data.target);
});

// 그리기를 취소할 경우 저장하기 버튼을 비활성화합니다
manager.addListener('cancel', function (e) {
  storageBtn.disabled = true;
  storageBtn.innerText = '저장하기';
  storageBtn.value = 'create';
  nameInput.disabled = true;
  nameInput.value = '';
});

// 그리기 요소를 삭제할 경우 저장하기 버튼을 비활성화합니다
manager.addListener('remove', function (e) {
  storageBtn.disabled = true;
  storageBtn.innerText = '저장하기';
  storageBtn.value = 'create';
  nameInput.disabled = true;
  nameInput.value = '';
});

// 그리기 요소를 선택할 경우 저장하기 버튼을 비활성화합니다
manager.addListener('select', function (e) {
  storageBtn.disabled = true;
  storageBtn.innerText = '저장하기';
  storageBtn.value = 'create';
  nameInput.disabled = true;
  nameInput.value = '';
});

// 그려진 객체 데이터를 DB에 저장하는 함수입니다
function dataStorage() {
  let type = storage.value;
  let name = nameInput.value;
  type == 'create' ? mapCreateRequest(name) : mapUpdateRequest(name);
}

// Drawing Manager에서 가져온 데이터 중 선을 아래 지도에 표시하는 함수입니다
function drawPolyline(lines) {
  let path = pointsToPath(lines.points);
  manager.put(kakao.maps.drawing.OverlayType.POLYLINE, path);
}

// Drawing Manager에서 가져온 데이터 중 다각형을 아래 지도에 표시하는 함수입니다
function drawPolygon(polygons) {
  let path = pointsToPath(polygons.points);
  manager.put(kakao.maps.drawing.OverlayType.POLYGON, path);
}

// 선과 다각형의 꼭지점 정보를 kakao.maps.LatLng객체로 생성하고 배열로 반환하는 함수입니다
function pointsToPath(points) {
  let len = points.length,
    path = [],
    i = 0;

  for (; i < len; i++) {
    // point[i][1] == y값, point[i][0] == x값
    let latlng = new kakao.maps.LatLng(points[i][1], points[i][0]);
    path.push(latlng);
  }

  return path;
}
