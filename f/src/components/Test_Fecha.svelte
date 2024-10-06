<script>
    let dateValue = new Date ("2024-09-27");

    let data =''
    let format = 'DD/MM/YYYY';
    let date = new Date(); // Date
    const onchange = ({ detail }) => {
        dateValue = detail
        console.log('onchange', detail);
    };

    function comprobar_fecha () {

        fetch('http://localhost:8000/api/comprobar_fecha/', {
            method: 'POST',
            headers: {
                "Authorization": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYSIsImV4cCI6MTcyODIyMTIwMH0.MMmu-iwWMkUafHu09Mcw-fAGFAjWrGu-f6cjDhmxaCQ",
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                "fecha": dateValue.toISOString(),
                "pk_viaje": "1",
            })
            
        })
        .then(response => response.json())
        .then(data => console.log('Comprobar fecha: ', data))
        .catch(error => console.error('Error:', error));
    }
</script>

<button on:click={comprobar_fecha}>Comprobar Fecha</button>
{data}
<style>

</style>