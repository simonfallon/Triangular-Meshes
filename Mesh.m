trimesh(Tgs, Pts(:,1), Pts(:,2), Pts(:,3));
V=vecindad(Tgs, Pts);
function V = vecindad (Tgs, Pts)
      for i=1:size(Pts(:,1))
             V(i,:)=[ i];
      end
      for i=1:size(Tgs(:,1))
          for j=1:3
              for k=j+1:3
                  if(~ismember(Tgs(i,j),V(Tgs(i,k))))
                        V(Tgs(i,k), end+1)=Tgs(i,j);
                  end
                  if(~ismember(Tgs(i,k),V(Tgs(i,j))))
                        V(Tgs(i,j), end+1)=Tgs(i,k);
                  end
              end
          end    
      end
end


