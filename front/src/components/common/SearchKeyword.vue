<template>
 <v-card dark color="#110b22"
 >

      <v-card-actions class='px-0'>
      <v-list-item class="grow px-2 py-0">
        <v-btn icon class="mx-1" large>

      <v-icon>mdi-pound</v-icon>
        </v-btn>
        <v-list-item-content>
          <v-list-item-title><span> 
            {{keyword}}
            </span>
            </v-list-item-title>

        </v-list-item-content>
      </v-list-item>
    </v-card-actions>
              </v-card>
</template>

<script>
    export default {
        props:{
            keyword:{
                type:String,
                default:'에러코드:관리자에게문의',
            },
            

        },
    
    }
</script>
